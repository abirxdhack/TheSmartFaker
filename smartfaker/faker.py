#Copyright @ISmartCoder
#Updates Channel t.me/TheSmartDev

import json
import random
from importlib.resources import files
import pycountry
import asyncio

class Faker:
    def __init__(self):
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
        countries = []
        for code in self._data.keys():
            display_code = 'GB' if code == 'uk' else code.upper()
            country = pycountry.countries.get(alpha_2=display_code)
            country_name = country.name if country else "Unknown"
            countries.append({"country_code": display_code, "country_name": country_name})
        return sorted(countries, key=lambda x: x["country_name"])

    async def address(self, country_code, amount=1, fields=None, locale=None):
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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.address(country_code, amount, fields, locale))
        finally:
            loop.close()

    async def batch_addresses(self, country_codes, amount=1, fields=None, locale=None):
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