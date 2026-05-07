Generate an Address
===================

The :meth:`~smartfaker.Faker.address` method returns one or more fake postal
addresses for a given ISO 3166-1 alpha-2 country code.

Single address
--------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("us")
    print(addr["city"], addr["zip"])

Multiple addresses
------------------

Pass ``amount=N`` to receive a list:

.. code-block:: python

    addrs = faker.address("fr", amount=5)
    for a in addrs:
        print(a["city"])

Async
-----

.. code-block:: python

    import asyncio

    async def main():
        addr = await faker.aaddress("jp")
        print(addr["city"])

    asyncio.run(main())

Response shape
--------------

Each address dict carries country-specific fields plus three metadata keys:

- ``api_owner`` — attribution string
- ``api_updates`` — update channel
- ``country_flag`` — regional-indicator emoji flag (e.g. ``"🇺🇸"``)

See :doc:`../advanced/response-schema` for the full schema.
