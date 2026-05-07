"""SmartFaker — Fake address & IBAN generator for 200+ countries.

A lightweight Python library for generating realistic fake postal addresses
and IBAN numbers across hundreds of countries and territories. Bundled
country data, zero network calls, and a true sync **and** async API.

Public API consists of the single :class:`Faker` class with methods for both
synchronous and asynchronous use:

Synchronous
-----------

* :meth:`Faker.address` — fake address for a single country.
* :meth:`Faker.batch_addresses` — fake addresses for many countries at once.
* :meth:`Faker.iban` — generate one or more valid IBANs.

Asynchronous
------------

* :meth:`Faker.aaddress` — async variant of :meth:`Faker.address`.
* :meth:`Faker.abatch_addresses` — async variant of :meth:`Faker.batch_addresses`.
* :meth:`Faker.aiban` — async variant of :meth:`Faker.iban`.

Example — Sync
--------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("us")
    iban = faker.iban("DE")
    print(addr["city"], iban["iban"])

Example — Async
---------------

.. code-block:: python

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    async def main():
        addr = await faker.aaddress("gb")
        iban = await faker.aiban("FR")
        print(addr["city"], iban["iban"])

    asyncio.run(main())

Documentation site: https://abirxdhack.github.io/TheSmartFaker
"""

from .fake import Faker

__version__ = "3.25.6"
__author__ = "ISmartCoder"
__license__ = "LGPL-3.0-or-later"
__all__ = ["Faker", "__version__"]
