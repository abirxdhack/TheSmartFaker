Batch Generation
================

When you need data for many countries in one call, use
:meth:`~smartfaker.Faker.batch_addresses`.

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    results = faker.batch_addresses(["us", "gb", "de", "fr"], amount=3)

    for code, addrs in results.items():
        print(code, len(addrs), "addresses")

Invalid country codes are skipped silently — the returned dict only
contains the codes that succeeded.

Async batch
-----------

.. code-block:: python

    import asyncio

    async def main():
        results = await faker.abatch_addresses(["us", "gb", "de", "fr"], amount=3)
        return results

    asyncio.run(main())

Concurrent IBAN batch
---------------------

For IBAN generation across many countries, drive the async API with
:func:`asyncio.gather`:

.. code-block:: python

    import asyncio

    async def fan_out():
        codes = ["DE", "GB", "FR", "ES", "IT"]
        tasks = [faker.aiban(c, amount=2) for c in codes]
        return dict(zip(codes, await asyncio.gather(*tasks)))

    asyncio.run(fan_out())
