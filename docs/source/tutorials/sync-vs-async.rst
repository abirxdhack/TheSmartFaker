Sync vs Async
=============

SmartFaker exposes every public generator twice: once as a synchronous
method and once as an ``a``-prefixed coroutine. Both share identical
signatures and return the same shape — pick whichever fits your call site.

============================  =================================
Synchronous                   Asynchronous
============================  =================================
``Faker.address``             ``Faker.aaddress``
``Faker.batch_addresses``     ``Faker.abatch_addresses``
``Faker.iban``                ``Faker.aiban``
``iban.calculate_check_digits``  ``iban.acalculate_check_digits``
``iban.validate_iban``        ``iban.avalidate_iban``
``iban.generate_numeric``     ``iban.agenerate_numeric``
``iban.generate_alpha``       ``iban.agenerate_alpha``
``iban.generate_alphanum``    ``iban.agenerate_alphanum``
============================  =================================

How the async wrappers work
---------------------------

The async methods on :class:`~smartfaker.Faker` dispatch the synchronous
implementation to a background thread via :func:`asyncio.to_thread`. This
keeps the event loop free even when callers fan out hundreds of concurrent
requests::

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    async def burst():
        return await asyncio.gather(*[faker.aiban("DE") for _ in range(50)])

    asyncio.run(burst())

When to choose which
--------------------

- **Scripts, CLI tools, notebooks** — use the sync API. Less ceremony.
- **Web frameworks (FastAPI, Sanic, aiohttp), async bots** — use the async
  API. It cooperates with the event loop and avoids "blocking call inside
  coroutine" warnings.
- **Mixed code** — both APIs are reentrant and thread-safe; mix freely.

Reusing a single instance
-------------------------

A :class:`~smartfaker.Faker` instance loads ~200 JSON files at construction
time. Build it **once** at process start and share it everywhere.
