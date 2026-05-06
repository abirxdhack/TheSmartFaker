# Copyright @ISmartCoder
# Updates Channel t.me/TheSmartDev

"""
SmartFaker - Fake address and IBAN generator for 200+ countries.

A lightweight, async-first Python library for generating realistic fake
addresses and IBAN numbers across hundreds of countries and territories.

Example::

    from smartfaker import Faker

    faker = Faker()

    # Async usage
    import asyncio
    addr = asyncio.run(faker.address("us"))

    # Sync usage
    addr = faker.address_sync("gb")
    iban = faker.iban_sync("DE")
"""

__version__ = "3.25.3"
__author__ = "ISmartCoder"
__license__ = "LGPL-3.0-or-later"

from .fake import Faker

__all__ = ["Faker", "__version__"]
