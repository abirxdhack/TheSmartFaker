Quickstart
==========

Install SmartFaker from PyPI::

    pip install smartfaker

Generate a fake address (sync)
------------------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("us")
    print(addr["city"], addr["zip"])

Generate a fake IBAN (sync)
---------------------------

.. code-block:: python

    iban = faker.iban("DE")
    print(iban["iban"])
    print(iban["details"])

Async usage
-----------

Every generation method has an ``a``-prefixed coroutine variant. They share
identical signatures and return values with the synchronous methods.

.. code-block:: python

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    async def main():
        addr = await faker.aaddress("gb")
        iban = await faker.aiban("FR")
        print(addr["city"], iban["iban"])

    asyncio.run(main())

Batch generation
----------------

.. code-block:: python

    results = faker.batch_addresses(["us", "gb", "de", "fr"], amount=2)
    for code, addrs in results.items():
        print(code, [a["city"] for a in addrs])

List supported countries
------------------------

.. code-block:: python

    for c in faker.countries():
        print(c["country_code"], c["country_name"])

    for c in faker.iban_countries():
        print(c["country_code"], c["country_name"])
