"""
Core Faker class for SmartFaker.

This module provides the :class:`Faker` class, which is the main entry point
for generating fake addresses and IBAN numbers. Data is loaded at construction
time from the bundled per-country JSON files under ``smartfaker/data/``.

Example::

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    countries = faker.countries()

    addr = asyncio.run(faker.address("us"))

    addr = faker.address_sync("gb")

    iban = faker.iban_sync("DE")

    addrs = asyncio.run(faker.address("fr", amount=5))
"""

import json
import random
import asyncio
from pathlib import Path

try:
    from importlib.resources import files as _resources_files
except ImportError:
    try:
        from importlib_resources import files as _resources_files
    except ImportError:
        _resources_files = None

import pycountry

from .iban import (
    bank_codes_data,
    country_data,
    COUNTRY_GENERATORS,
    letter_to_number,
    generate_numeric,
    generate_alphanum,
    calculate_check_digits,
    validate_iban,
)


class Faker:
    """Generate realistic fake addresses and IBAN numbers for 200+ countries.

    Addresses are loaded from bundled JSON data files. IBAN generation uses
    country-specific algorithms conforming to the ISO 13616 standard.

    All address methods have both ``async`` and sync (``_sync``) variants so
    the class works in both asyncio and synchronous contexts.

    Attributes:
        _data (dict): Mapping of lowercase country code to a list of address
            dictionaries loaded from the bundled JSON files.

    Example::

        from smartfaker import Faker

        faker = Faker()
        addr = faker.address_sync("us")
        iban = faker.iban_sync("DE")
    """

    def __init__(self):
        """Initialize SmartFaker and load all bundled address data files.

        Scans ``smartfaker/data/*.json`` from the package directory and
        populates the internal ``_data`` mapping. Files that fail JSON
        parsing are silently skipped. Works on Python 3.8 and newer by
        gracefully falling back to :mod:`pathlib` when
        :func:`importlib.resources.files` is unavailable.
        """
        self._data: dict = {}
        if _resources_files is not None:
            try:
                data_root = _resources_files("smartfaker").joinpath("data")
                entries = list(data_root.iterdir())
            except (ModuleNotFoundError, FileNotFoundError, AttributeError):
                data_root = Path(__file__).resolve().parent / "data"
                entries = list(data_root.iterdir())
        else:
            data_root = Path(__file__).resolve().parent / "data"
            entries = list(data_root.iterdir())
        for file_path in entries:
            name = getattr(file_path, "name", str(file_path))
            if not name.endswith(".json"):
                continue
            stem = name[:-5]
            country_code = stem.upper()
            file_country_code = "uk" if country_code == "UK" else country_code.lower()
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    self._data[file_country_code] = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue

    def countries(self) -> list:
        """Return a sorted list of countries available for address generation.

        Returns:
            list[dict]: Each item has ``"country_code"`` (ISO alpha-2, e.g.
            ``"US"``) and ``"country_name"`` (e.g. ``"United States"``),
            sorted alphabetically by name.

        Example::

            countries = faker.countries()
        """
        result = []
        for code in self._data.keys():
            display_code = "GB" if code == "uk" else code.upper()
            country = pycountry.countries.get(alpha_2=display_code)
            country_name = country.name if country else "Unknown"
            result.append({"country_code": display_code, "country_name": country_name})
        return sorted(result, key=lambda x: x["country_name"])

    async def address(
        self,
        country_code: str,
        amount: int = 1,
        fields: list = None,
        locale: str = None,
    ):
        """Generate one or more fake addresses for a given country.

        Args:
            country_code (str): ISO 3166-1 alpha-2 country code (case-insensitive),
                e.g. ``"us"``, ``"GB"``, ``"fr"``.
            amount (int): Number of addresses to generate. Defaults to ``1``.
                Capped at the number of available records for the country.
            fields (list[str] | None): If given, only these keys are included
                in each returned address dict. Defaults to all fields.
            locale (str | None): If given, prefixes the ``person_name`` field
                with ``"<locale>_"``. Defaults to ``None``.

        Returns:
            dict | list[dict]: A single address dict when ``amount=1``, or a
            list of address dicts otherwise. Every dict includes an
            ``"api_owner"``, ``"api_updates"``, and ``"country_flag"`` field.

        Raises:
            ValueError: If ``country_code`` is empty or not in the dataset.

        Example::

            addr = await faker.address("us")
            five = await faker.address("fr", amount=5, fields=["city", "zip"])
        """
        if not country_code:
            raise ValueError("Country code is required")
        code = country_code.lower()
        if code not in self._data:
            raise ValueError(f"Invalid country code: {country_code}")
        addresses = self._data[code]
        if not addresses:
            raise ValueError(f"No addresses available for {country_code}")
        result = []
        for _ in range(min(amount, len(addresses))):
            addr = random.choice(addresses).copy()
            addr["api_owner"] = "@ISmartCoder"
            addr["api_updates"] = "t.me/TheSmartDev"
            addr["country_flag"] = "".join(
                chr(0x1F1E6 + ord(c) - ord("A")) for c in country_code.upper()
            )
            if fields:
                addr = {k: v for k, v in addr.items() if k in fields}
            if locale and "person_name" in addr:
                addr["person_name"] = f"{locale}_{addr['person_name']}"
            result.append(addr)
        return result[0] if amount == 1 else result

    def address_sync(
        self,
        country_code: str,
        amount: int = 1,
        fields: list = None,
        locale: str = None,
    ):
        """Synchronous wrapper around :meth:`address`.

        Creates a fresh event loop, runs :meth:`address`, and closes the loop.
        Use this in scripts or frameworks that do not provide an event loop.

        Args:
            country_code (str): ISO 3166-1 alpha-2 country code.
            amount (int): Number of addresses to generate. Defaults to ``1``.
            fields (list[str] | None): Subset of fields to include.
            locale (str | None): Locale prefix for ``person_name``.

        Returns:
            dict | list[dict]: Same as :meth:`address`.

        Example::

            addr = faker.address_sync("gb")
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.address(country_code, amount, fields, locale))
        finally:
            loop.close()

    async def batch_addresses(
        self,
        country_codes: list,
        amount: int = 1,
        fields: list = None,
        locale: str = None,
    ) -> dict:
        """Generate addresses for multiple countries in one call.

        Invalid country codes are silently skipped.

        Args:
            country_codes (list[str]): List of ISO 3166-1 alpha-2 codes.
            amount (int): Addresses per country. Defaults to ``1``.
            fields (list[str] | None): Subset of fields to include.
            locale (str | None): Locale prefix for ``person_name``.

        Returns:
            dict: Mapping of uppercase country code to the address result(s).
                Countries that fail are omitted.

        Raises:
            ValueError: If ``country_codes`` is empty or ``None``.

        Example::

            results = await faker.batch_addresses(["us", "gb", "de"])
            us_addr = results["US"]
        """
        if not country_codes:
            raise ValueError("At least one country code is required")
        results = {}
        for code in country_codes:
            try:
                addr = await self.address(code, amount, fields, locale)
                results[code.upper()] = addr
            except ValueError:
                continue
        return results

    async def iban(self, country_code: str, amount: int = 1):
        """Generate one or more valid fake IBANs for a given country.

        Uses the country-specific BBAN generator and MOD-97 check-digit
        algorithm to produce structurally valid IBANs.

        Args:
            country_code (str): ISO 3166-1 alpha-2 country code (uppercase),
                e.g. ``"DE"``, ``"GB"``, ``"US"``.
            amount (int): Number of IBANs to generate. Defaults to ``1``.

        Returns:
            dict | list[dict]: A single IBAN result dict when ``amount=1``,
            or a list otherwise. Each dict contains:

            - ``iban`` — the full IBAN string
            - ``country`` — the country code
            - ``valid`` — always ``True``
            - ``length`` — total length of the IBAN
            - ``details`` — parsed BBAN fields (bank code, account number, etc.)
            - ``api_owner`` — attribution field
            - ``api_updates`` — update channel

        Raises:
            ValueError: If ``country_code`` is empty, unsupported, or if the
                generated IBAN fails length or MOD-97 validation.

        Example::

            iban = await faker.iban("DE")
            ibans = await faker.iban("GB", amount=3)
        """
        if not country_code:
            raise ValueError("Country code is required")
        code = country_code.upper()
        if code not in COUNTRY_GENERATORS:
            raise ValueError(f"Invalid country code: {country_code}")
        result = []
        for _ in range(amount):
            bban = await COUNTRY_GENERATORS[code]["generator"]()
            check_digits = await calculate_check_digits(code, bban)
            iban_str = f"{code}{check_digits}{bban}"
            if len(iban_str) != COUNTRY_GENERATORS[code]["length"]:
                raise ValueError(f"Generated IBAN length mismatch for {country_code}")
            if not await validate_iban(iban_str):
                raise ValueError(f"Generated IBAN is invalid for {country_code}")
            details = {"bban": bban, "check_digits": check_digits}
            data = country_data[code]
            offset = 0
            if "bank_codes" in data:
                details["bank_code"] = bban[: len(data["bank_codes"][0])]
                offset = len(data["bank_codes"][0])
            elif "bank_code_length" in data:
                details["bank_code"] = bban[: data["bank_code_length"]]
                offset = data["bank_code_length"]
            if "branch_code_length" in data:
                details["branch_code"] = bban[offset : offset + data["branch_code_length"]]
                offset += data["branch_code_length"]
            if "sort_code_length" in data:
                details["sort_code"] = bban[offset : offset + data["sort_code_length"]]
                offset += data["sort_code_length"]
            if "prefix_length" in data:
                details["prefix"] = bban[offset : offset + data["prefix_length"]]
                offset += data["prefix_length"]
            if "type_code_length" in data:
                details["type_code"] = bban[offset : offset + data["type_code_length"]]
                offset += data["type_code_length"]
            if "identification_length" in data:
                details["identification_number"] = bban[offset : offset + data["identification_length"]]
                offset += data["identification_length"]
            if "check_digits_length" in data:
                details["check_digits"] = bban[offset : offset + data["check_digits_length"]]
                offset += data["check_digits_length"]
            if "key_length" in data:
                details["key"] = bban[offset : offset + data["key_length"]]
                offset += data["key_length"]
            if "account_type_length" in data:
                details["account_type"] = bban[offset : offset + data["account_type_length"]]
                offset += data["account_type_length"]
            if "owner_type_length" in data:
                details["owner_type"] = bban[offset : offset + data["owner_type_length"]]
                offset += data["owner_type_length"]
            if "reserved_length" in data:
                details["reserved"] = bban[offset : offset + data["reserved_length"]]
                offset += data["reserved_length"]
            if "account_length" in data:
                details["account_number"] = bban[offset : offset + data["account_length"]]
            if "check_char" in data and data["check_char"]:
                details["cin"] = bban[0]
            result.append(
                {
                    "iban": iban_str,
                    "country": code,
                    "valid": True,
                    "length": len(iban_str),
                    "details": details,
                    "api_owner": "@ISmartCoder",
                    "api_updates": "t.me/TheSmartDev",
                }
            )
        return result[0] if amount == 1 else result

    def iban_sync(self, country_code: str, amount: int = 1):
        """Synchronous wrapper around :meth:`iban`.

        Args:
            country_code (str): ISO 3166-1 alpha-2 country code.
            amount (int): Number of IBANs to generate. Defaults to ``1``.

        Returns:
            dict | list[dict]: Same as :meth:`iban`.

        Example::

            iban = faker.iban_sync("DE")
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.iban(country_code, amount))
        finally:
            loop.close()

    def iban_countries(self) -> list:
        """Return a sorted list of countries supported for IBAN generation.

        Returns:
            list[dict]: Each item has ``"country_code"`` and ``"country_name"``,
            sorted alphabetically by name.

        Example::

            iban_countries = faker.iban_countries()
        """
        result = []
        for code in COUNTRY_GENERATORS.keys():
            country = pycountry.countries.get(alpha_2=code)
            country_name = country.name if country else "Unknown"
            result.append({"country_code": code, "country_name": country_name})
        return sorted(result, key=lambda x: x["country_name"])
