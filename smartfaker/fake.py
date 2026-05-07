"""Core Faker class for SmartFaker.

This module provides :class:`Faker`, the main entry point for generating
fake addresses and IBAN numbers. Address records are loaded once at
construction from the bundled per-country JSON files under
``smartfaker/data/``.

Every public generator method comes in two flavours, mirroring the
:mod:`smartbindb` API style:

* Synchronous methods — :meth:`Faker.address`, :meth:`Faker.batch_addresses`,
  :meth:`Faker.iban`. Safe to call from any synchronous code path.
* Asynchronous methods — :meth:`Faker.aaddress`,
  :meth:`Faker.abatch_addresses`, :meth:`Faker.aiban`. Coroutines that
  delegate to the sync implementations via :func:`asyncio.to_thread` so they
  never block the event loop.

Example — sync::

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("us")
    iban = faker.iban("DE")

Example — async::

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    async def main():
        addr = await faker.aaddress("gb")
        iban = await faker.aiban("FR")
        print(addr["city"], iban["iban"])

    asyncio.run(main())
"""

import asyncio
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

try:
    from importlib.resources import files as _resources_files
except ImportError:
    try:
        from importlib_resources import files as _resources_files
    except ImportError:
        _resources_files = None

import pycountry

from .iban import (
    COUNTRY_GENERATORS,
    calculate_check_digits,
    country_data,
    validate_iban,
)

API_OWNER = "@ISmartCoder"
API_UPDATES = "t.me/TheSmartDev"

T = TypeVar("T")

if sys.version_info >= (3, 9):
    async def _to_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        return await asyncio.to_thread(func, *args, **kwargs)
else:
    async def _to_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(func, *args, **kwargs)
        )


def _country_flag(country_code: str) -> str:
    """Return the regional-indicator emoji flag for an ISO alpha-2 code."""
    code = country_code.upper()
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code)


class Faker:
    """Generate realistic fake addresses and IBAN numbers for 200+ countries.

    Addresses are loaded from bundled JSON data files. IBAN generation uses
    country-specific algorithms conforming to ISO 13616 with MOD-97 check
    digits.

    All public generation methods have **both** synchronous and asynchronous
    variants. The asynchronous (``a``-prefixed) methods run their synchronous
    counterparts on the default executor via :func:`asyncio.to_thread`, so
    they integrate cleanly with any ``asyncio`` framework without blocking
    the event loop.

    Attributes:
        data (dict[str, list[dict]]): Mapping of lowercase ISO alpha-2
            country code to the list of address dictionaries loaded from the
            bundled JSON files.

    Example::

        from smartfaker import Faker

        faker = Faker()
        addr = faker.address("us")
        iban = faker.iban("DE")
    """

    def __init__(self) -> None:
        """Initialize SmartFaker and load all bundled address data files.

        Scans ``smartfaker/data/*.json`` from the package directory and
        populates :attr:`data`. Files that fail JSON parsing are silently
        skipped so a single corrupt file cannot break the whole loader.
        Works on Python 3.8+ by gracefully falling back to :mod:`pathlib`
        when :func:`importlib.resources.files` is unavailable.
        """
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        entries = self._iter_data_files()
        for file_path in entries:
            name = getattr(file_path, "name", str(file_path))
            if not name.endswith(".json"):
                continue
            stem = name[:-5]
            country_code = "uk" if stem.lower() == "uk" else stem.lower()
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    self.data[country_code] = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue

    # Backwards-compat alias for older internal users.
    @property
    def _data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Deprecated alias for :attr:`data`. Kept for backwards compatibility."""
        return self.data

    @staticmethod
    def _iter_data_files():
        """Yield path-like objects for every bundled address JSON file."""
        if _resources_files is not None:
            try:
                root = _resources_files("smartfaker").joinpath("data")
                return list(root.iterdir())
            except (ModuleNotFoundError, FileNotFoundError, AttributeError):
                pass
        root = Path(__file__).resolve().parent / "data"
        return list(root.iterdir())

    # ------------------------------------------------------------------ helpers

    def _decorate(
        self,
        addr: Dict[str, Any],
        country_code: str,
        fields: Optional[List[str]],
        locale: Optional[str],
    ) -> Dict[str, Any]:
        """Add metadata, optionally filter fields, and apply locale prefix."""
        decorated = dict(addr)
        decorated["api_owner"] = API_OWNER
        decorated["api_updates"] = API_UPDATES
        decorated["country_flag"] = _country_flag(country_code)
        if locale and "person_name" in decorated:
            decorated["person_name"] = f"{locale}_{decorated['person_name']}"
        if fields:
            decorated = {k: v for k, v in decorated.items() if k in fields}
        return decorated

    def _resolve_country(self, country_code: str) -> str:
        if not country_code:
            raise ValueError("Country code is required")
        code = country_code.lower()
        if code not in self.data:
            raise ValueError(f"Invalid country code: {country_code}")
        if not self.data[code]:
            raise ValueError(f"No addresses available for {country_code}")
        return code

    # ------------------------------------------------------------------ public

    def countries(self) -> List[Dict[str, str]]:
        """Return the sorted list of countries available for address generation.

        Returns:
            list[dict]: Each item has ``"country_code"`` (ISO alpha-2, e.g.
            ``"US"``) and ``"country_name"`` (e.g. ``"United States"``),
            sorted alphabetically by country name.

        Example::

            faker = Faker()
            for c in faker.countries():
                print(c["country_code"], c["country_name"])
        """
        result = []
        for code in self.data.keys():
            display_code = "GB" if code == "uk" else code.upper()
            country = pycountry.countries.get(alpha_2=display_code)
            country_name = country.name if country else "Unknown"
            result.append({"country_code": display_code, "country_name": country_name})
        return sorted(result, key=lambda x: x["country_name"])

    def iban_countries(self) -> List[Dict[str, str]]:
        """Return the sorted list of countries supported for IBAN generation.

        Returns:
            list[dict]: Each item has ``"country_code"`` and
            ``"country_name"``, sorted alphabetically by country name.

        Example::

            for c in faker.iban_countries():
                print(c["country_code"], c["country_name"])
        """
        result = []
        for code in COUNTRY_GENERATORS.keys():
            country = pycountry.countries.get(alpha_2=code)
            country_name = country.name if country else "Unknown"
            result.append({"country_code": code, "country_name": country_name})
        return sorted(result, key=lambda x: x["country_name"])

    # ------------------------------------------------------------- addresses

    def address(
        self,
        country_code: str,
        amount: int = 1,
        fields: Optional[List[str]] = None,
        locale: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Generate one or more fake addresses for a given country (synchronous).

        Args:
            country_code: ISO 3166-1 alpha-2 country code (case-insensitive),
                e.g. ``"us"``, ``"GB"``, ``"fr"``.
            amount: Number of addresses to generate. Defaults to ``1``. Capped
                at the number of records available for the country.
            fields: If given, only these keys are kept in each returned
                address dictionary.
            locale: If given, prefixes the ``person_name`` field with
                ``"<locale>_"``.

        Returns:
            A single address ``dict`` when ``amount=1``, otherwise a ``list``
            of address dicts. Every dict carries ``api_owner``,
            ``api_updates`` and ``country_flag`` metadata.

        Raises:
            ValueError: If ``country_code`` is empty, unknown, or has no
                bundled records.

        Example::

            addr = faker.address("us")
            five = faker.address("fr", amount=5, fields=["city", "zip"])
        """
        code = self._resolve_country(country_code)
        records = self.data[code]
        n = max(1, min(amount, len(records)))
        result = [
            self._decorate(random.choice(records), country_code, fields, locale)
            for _ in range(n)
        ]
        return result[0] if amount == 1 else result

    async def aaddress(
        self,
        country_code: str,
        amount: int = 1,
        fields: Optional[List[str]] = None,
        locale: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Asynchronous variant of :meth:`address`.

        Identical contract to :meth:`address`; the call is dispatched to a
        worker thread so it never blocks the event loop.

        Example::

            addr = await faker.aaddress("us")
        """
        return await _to_thread(self.address, country_code, amount, fields, locale)

    def batch_addresses(
        self,
        country_codes: List[str],
        amount: int = 1,
        fields: Optional[List[str]] = None,
        locale: Optional[str] = None,
    ) -> Dict[str, Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """Generate addresses for multiple countries in one call (synchronous).

        Invalid or unsupported country codes are silently skipped.

        Args:
            country_codes: List of ISO 3166-1 alpha-2 codes.
            amount: Addresses per country. Defaults to ``1``.
            fields: Subset of fields to include in each address dictionary.
            locale: Locale prefix for ``person_name``.

        Returns:
            dict: Mapping of uppercase country code to the address result(s)
            for that country. Countries that fail are omitted.

        Raises:
            ValueError: If ``country_codes`` is empty or ``None``.

        Example::

            results = faker.batch_addresses(["us", "gb", "de"])
            us_addr = results["US"]
        """
        if not country_codes:
            raise ValueError("At least one country code is required")
        results: Dict[str, Union[Dict[str, Any], List[Dict[str, Any]]]] = {}
        for code in country_codes:
            try:
                results[code.upper()] = self.address(code, amount, fields, locale)
            except ValueError:
                continue
        return results

    async def abatch_addresses(
        self,
        country_codes: List[str],
        amount: int = 1,
        fields: Optional[List[str]] = None,
        locale: Optional[str] = None,
    ) -> Dict[str, Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """Asynchronous variant of :meth:`batch_addresses`.

        Example::

            results = await faker.abatch_addresses(["us", "gb"])
        """
        return await _to_thread(
            self.batch_addresses, country_codes, amount, fields, locale
        )

    # ------------------------------------------------------------------ IBAN

    def iban(
        self, country_code: str, amount: int = 1
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Generate one or more valid fake IBANs for a given country (synchronous).

        Uses the country-specific BBAN generator and the MOD-97 check-digit
        algorithm to produce structurally valid IBANs. Generated IBANs are
        re-validated before being returned.

        Args:
            country_code: ISO 3166-1 alpha-2 country code (uppercase),
                e.g. ``"DE"``, ``"GB"``, ``"US"``.
            amount: Number of IBANs to generate. Defaults to ``1``.

        Returns:
            A single result ``dict`` when ``amount=1``, otherwise a ``list``
            of result dicts. Each dict contains:

            - ``iban``: full IBAN string
            - ``country``: country code
            - ``valid``: always ``True``
            - ``length``: total length of the IBAN
            - ``details``: parsed BBAN fields (bank code, account number, …)
            - ``api_owner`` / ``api_updates``: attribution

        Raises:
            ValueError: If ``country_code`` is empty, unsupported, or if the
                generated IBAN fails length or MOD-97 validation.

        Example::

            iban = faker.iban("DE")
            ibans = faker.iban("GB", amount=3)
        """
        if not country_code:
            raise ValueError("Country code is required")
        code = country_code.upper()
        if code not in COUNTRY_GENERATORS:
            raise ValueError(f"Invalid country code: {country_code}")
        spec = COUNTRY_GENERATORS[code]
        result: List[Dict[str, Any]] = []
        for _ in range(max(1, amount)):
            bban = spec["generator"]()
            check_digits = calculate_check_digits(code, bban)
            iban_str = f"{code}{check_digits}{bban}"
            if len(iban_str) != spec["length"]:
                raise ValueError(f"Generated IBAN length mismatch for {country_code}")
            if not validate_iban(iban_str):
                raise ValueError(f"Generated IBAN is invalid for {country_code}")
            details: Dict[str, Any] = {"bban": bban, "check_digits": check_digits}
            data = country_data[code]
            offset = 0
            if "bank_codes" in data:
                bc_len = len(data["bank_codes"][0])
                details["bank_code"] = bban[:bc_len]
                offset = bc_len
            elif "bank_code_length" in data:
                details["bank_code"] = bban[: data["bank_code_length"]]
                offset = data["bank_code_length"]
            for key, label in (
                ("branch_code_length", "branch_code"),
                ("sort_code_length", "sort_code"),
                ("prefix_length", "prefix"),
                ("type_code_length", "type_code"),
                ("identification_length", "identification_number"),
                ("check_digits_length", "check_digits"),
                ("key_length", "key"),
                ("account_type_length", "account_type"),
                ("owner_type_length", "owner_type"),
                ("reserved_length", "reserved"),
            ):
                if key in data:
                    details[label] = bban[offset : offset + data[key]]
                    offset += data[key]
            if "account_length" in data:
                details["account_number"] = bban[offset : offset + data["account_length"]]
            if data.get("check_char"):
                details["cin"] = bban[0]
            result.append(
                {
                    "iban": iban_str,
                    "country": code,
                    "valid": True,
                    "length": len(iban_str),
                    "details": details,
                    "api_owner": API_OWNER,
                    "api_updates": API_UPDATES,
                }
            )
        return result[0] if amount == 1 else result

    async def aiban(
        self, country_code: str, amount: int = 1
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Asynchronous variant of :meth:`iban`.

        Example::

            iban = await faker.aiban("DE")
        """
        return await _to_thread(self.iban, country_code, amount)

    # ---------------------------------------------------- legacy compatibility

    def address_sync(self, *args, **kwargs):
        """Deprecated alias for :meth:`address` (kept for backwards compatibility)."""
        return self.address(*args, **kwargs)

    def iban_sync(self, *args, **kwargs):
        """Deprecated alias for :meth:`iban` (kept for backwards compatibility)."""
        return self.iban(*args, **kwargs)
