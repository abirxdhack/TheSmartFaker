# SmartFaker

**Fake address & IBAN generator for 200+ countries — sync & async Python library**

[![PyPI version](https://img.shields.io/pypi/v/smartfaker.svg)](https://pypi.org/project/smartfaker)
[![Python](https://img.shields.io/pypi/pyversions/smartfaker.svg)](https://pypi.org/project/smartfaker)
[![License](https://img.shields.io/pypi/l/smartfaker.svg)](https://pypi.org/project/smartfaker)

SmartFaker generates realistic fake postal addresses and IBAN numbers for
over 200 countries. Bundled data, zero network calls, and a true sync
**and** async API.

## Installation

```bash
pip install smartfaker
```

## Quick start — sync

```python
from smartfaker import Faker

faker = Faker()
addr = faker.address("us")
iban = faker.iban("DE")
print(addr["city"], iban["iban"])
```

## Quick start — async

```python
import asyncio
from smartfaker import Faker

faker = Faker()

async def main():
    addr = await faker.aaddress("gb")
    iban = await faker.aiban("FR")
    print(addr["city"], iban["iban"])

asyncio.run(main())
```

## Features

- **200+ countries** of bundled address data
- **57 country IBAN generators** with MOD-97 validation
- **Sync and async, both first-class** — `address` / `aaddress`,
  `batch_addresses` / `abatch_addresses`, `iban` / `aiban`
- **Field filtering** and **locale-prefixed names**
- **Batch generation** across many countries in one call
- **Tiny dependency surface** — only `pycountry`

## Documentation

- Full docs: <https://abirxdhack.github.io/TheSmartFaker>
- Repository: <https://github.com/abirxdhack/TheSmartFaker>

## License

LGPL-3.0-or-later © ISmartCoder | [t.me/TheSmartDev](https://t.me/TheSmartDev)
