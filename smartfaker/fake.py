#Copyright @ISmartCoder
#Updates Channel @TheSmartDev
import json
import random
from importlib.resources import files
import pycountry
import asyncio
from .iban import bank_codes_data, country_data, COUNTRY_GENERATORS, letter_to_number, generate_numeric, generate_alphanum, calculate_check_digits, validate_iban

class Faker:
    """A class for generating fake addresses and IBANs for various countries."""
    def __init__(self):
        """Initialize the Faker with address data from JSON files."""
        self._data = {}
        data_path = files('smartfaker.data')
        for file_path in data_path.iterdir():
            if file_path.is_file() and file_path.suffix == '.json':
                country_code = file_path.stem.upper()
                file_country_code = 'uk' if country_code == 'UK' else country_code.lower()
                with file_path.open('r', encoding='utf-8') as f:
                    try:
                        self._data[file_country_code] = json.load(f)
                    except json.JSONDecodeError:
                        continue

    def countries(self):
        """Return a sorted list of countries available for address generation."""
        countries = []
        for code in self._data.keys():
            display_code = 'GB' if code == 'uk' else code.upper()
            country = pycountry.countries.get(alpha_2=display_code)
            country_name = country.name if country else "Unknown"
            countries.append({"country_code": display_code, "country_name": country_name})
        return sorted(countries, key=lambda x: x["country_name"])

    async def address(self, country_code, amount=1, fields=None, locale=None):
        """Generate fake addresses for a given country code."""
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
            addr["country_flag"] = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())
            if fields:
                addr = {k: v for k, v in addr.items() if k in fields}
            if locale and "person_name" in addr:
                addr["person_name"] = f"{locale}_{addr['person_name']}"
            result.append(addr)
        return result[0] if amount == 1 else result

    def address_sync(self, country_code, amount=1, fields=None, locale=None):
        """Synchronous version of address generation."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.address(country_code, amount, fields, locale))
        finally:
            loop.close()

    async def batch_addresses(self, country_codes, amount=1, fields=None, locale=None):
        """Generate addresses for multiple country codes."""
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

    async def iban(self, country_code, amount=1):
        """Generate fake IBANs for a given country code."""
        if not country_code:
            raise ValueError("Country code is required")
        code = country_code.upper()
        if code not in COUNTRY_GENERATORS:
            raise ValueError(f"Invalid country code: {country_code}")
        result = []
        for _ in range(amount):
            bban = await COUNTRY_GENERATORS[code]["generator"]()
            check_digits = await calculate_check_digits(code, bban)
            iban = f"{code}{check_digits}{bban}"
            if len(iban) != COUNTRY_GENERATORS[code]["length"]:
                raise ValueError(f"Generated IBAN length mismatch for {country_code}")
            if not await validate_iban(iban):
                raise ValueError(f"Generated IBAN is invalid for {country_code}")
            details = {"bban": bban, "check_digits": check_digits}
            data = country_data[code]
            offset = 0
            if "bank_codes" in data:
                details["bank_code"] = bban[:len(data["bank_codes"][0])]
                offset = len(data["bank_codes"][0])
            elif "bank_code_length" in data:
                details["bank_code"] = bban[:data["bank_code_length"]]
                offset = data["bank_code_length"]
            if "branch_code_length" in data:
                details["branch_code"] = bban[offset:offset+data["branch_code_length"]]
                offset += data["branch_code_length"]
            if "sort_code_length" in data:
                details["sort_code"] = bban[offset:offset+data["sort_code_length"]]
                offset += data["sort_code_length"]
            if "prefix_length" in data:
                details["prefix"] = bban[offset:offset+data["prefix_length"]]
                offset += data["prefix_length"]
            if "type_code_length" in data:
                details["type_code"] = bban[offset:offset+data["type_code_length"]]
                offset += data["type_code_length"]
            if "identification_length" in data:
                details["identification_number"] = bban[offset:offset+data["identification_length"]]
                offset += data["identification_length"]
            if "check_digits_length" in data:
                details["check_digits"] = bban[offset:offset+data["check_digits_length"]]
                offset += data["check_digits_length"]
            if "key_length" in data:
                details["key"] = bban[offset:offset+data["key_length"]]
                offset += data["key_length"]
            if "account_type_length" in data:
                details["account_type"] = bban[offset:offset+data["account_type_length"]]
                offset += data["account_type_length"]
            if "owner_type_length" in data:
                details["owner_type"] = bban[offset:offset+data["owner_type_length"]]
                offset += data["owner_type_length"]
            if "reserved_length" in data:
                details["reserved"] = bban[offset:offset+data["reserved_length"]]
                offset += data["reserved_length"]
            if "account_length" in data:
                details["account_number"] = bban[offset:offset+data["account_length"]]
            if "check_char" in data and data["check_char"]:
                details["cin"] = bban[0]
            result.append({
                "iban": iban,
                "country": code,
                "valid": True,
                "length": len(iban),
                "details": details,
                "api_owner": "@ISmartCoder",
                "api_updates": "t.me/TheSmartDev"
            })
        return result[0] if amount == 1 else result

    def iban_sync(self, country_code, amount=1):
        """Synchronous version of IBAN generation."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.iban(country_code, amount))
        finally:
            loop.close()

    def iban_countries(self):
        """Return a sorted list of countries available for IBAN generation."""
        countries = []
        for code in COUNTRY_GENERATORS.keys():
            country = pycountry.countries.get(alpha_2=code)
            country_name = country.name if country else "Unknown"
            countries.append({"country_code": code, "country_name": country_name})
        return sorted(countries, key=lambda x: x["country_name"])
