Overview
========

SmartFaker is a zero-network, zero-config Python library for generating
realistic fake postal addresses and structurally valid IBAN numbers across
200+ countries and territories.

Design goals
------------

- **Bundled data** — every address record and IBAN format spec ships inside
  the wheel. The library never makes a network request.
- **Sync and async, both first-class** — every public generator method has a
  synchronous version and an ``a``-prefixed coroutine version. The async
  variants run on a worker thread via :func:`asyncio.to_thread` so they
  never block the event loop.
- **Tiny dependency surface** — the only runtime requirement is
  :mod:`pycountry`.
- **Predictable response schema** — address dicts always carry
  ``api_owner``, ``api_updates`` and ``country_flag`` metadata. IBAN dicts
  always carry ``iban``, ``country``, ``valid``, ``length`` and ``details``.

What's inside
-------------

- ~200 per-country address record sets under ``smartfaker/data/``
- 57 country-specific IBAN BBAN generators with MOD-97 validation
- A small amount of ISO metadata helpers built on :mod:`pycountry`

Use cases
---------

- Seeding test databases with realistic-looking customer records
- Generating sample bank account numbers for IBAN parser testing
- Building CLI tools that need throwaway data for demos
- Powering Telegram / Discord bots that demonstrate fake-data flows
