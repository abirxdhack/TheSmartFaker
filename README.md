# SmartFaker

**Fake address & IBAN generator for 200+ countries — async-first Python library**

[![PyPI version](https://img.shields.io/pypi/v/smartfaker.svg)](https://pypi.org/project/smartfaker)
[![Python](https://img.shields.io/pypi/pyversions/smartfaker.svg)](https://pypi.org/project/smartfaker)
[![License](https://img.shields.io/pypi/l/smartfaker.svg)](https://pypi.org/project/smartfaker)

SmartFaker generates realistic fake postal addresses and IBAN numbers for
over 200 countries. It is async-first with synchronous wrappers, requires no
external API, and ships bundled country data.

## Installation

```bash
pip install smartfaker
```

## Quick Start

```python
from smartfaker import Faker

faker = Faker()

# Sync usage
addr = faker.address_sync("us")
iban = faker.iban_sync("DE")

print(addr["city"], addr["zip"])
print(iban["iban"])
```

```python
# Async usage
import asyncio
from smartfaker import Faker

faker = Faker()

async def main():
    addr = await faker.address("gb")
    iban = await faker.iban("FR")
    print(addr, iban["iban"])

asyncio.run(main())
```

## Features

- **200+ countries** — bundled JSON address data for every country and territory
- **IBAN generation** — 57 countries with country-specific algorithms and MOD-97 validation
- **Async-first** — all generation methods are `async`; sync wrappers included
- **Field filtering** — request only the fields you need
- **Batch generation** — generate addresses for multiple countries in one call
- **Zero external dependencies** beyond `pycountry`

## Documentation

- GitHub Pages: https://abirxdhack.github.io/TheSmartFaker/
- Repository: https://github.com/abirxdhack/TheSmartFaker

## API

### Address generation

```python
# Single address
addr = faker.address_sync("us")

# Multiple addresses
addrs = faker.address_sync("fr", amount=5)

# Specific fields only
addr = faker.address_sync("de", fields=["city", "zip", "street"])

# Batch — multiple countries
import asyncio
results = asyncio.run(faker.batch_addresses(["us", "gb", "de"]))
```

### IBAN generation

```python
# Single IBAN
iban = faker.iban_sync("DE")
print(iban["iban"])     # DE...
print(iban["details"])  # {"bank_code": ..., "account_number": ...}

# Multiple IBANs
ibans = faker.iban_sync("GB", amount=3)

# List supported countries
for c in faker.iban_countries():
    print(c["country_code"], c["country_name"])
```

## License

LGPL-3.0-or-later © ISmartCoder | [t.me/TheSmartDev](https://t.me/TheSmartDev)
