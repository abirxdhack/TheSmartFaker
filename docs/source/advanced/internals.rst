Internals
=========

This page documents internal implementation details for contributors.
Public users should rely on :class:`smartfaker.Faker` and the helpers in
:mod:`smartfaker.iban` instead.

Module layout
-------------

- ``smartfaker/__init__.py`` — package metadata and re-exports.
- ``smartfaker/fake.py`` — :class:`Faker` and address generation.
- ``smartfaker/iban.py`` — bank code data, country format specs,
  per-country BBAN generators, MOD-97 helpers and async wrappers.
- ``smartfaker/data/`` — bundled per-country address JSON files.
- ``compiler/docs/compiler.py`` — auto-generates per-method / per-function
  RST pages under ``docs/source/api/``.

Async wrapper strategy
----------------------

Async methods on :class:`Faker` (``aaddress``, ``abatch_addresses``,
``aiban``) all dispatch their synchronous counterparts to
:func:`asyncio.to_thread`. This guarantees:

- the event loop never blocks, even for very large ``amount`` values;
- semantics, return shape and exceptions are bit-for-bit identical to the
  sync API — there is no second implementation to keep in sync.

The IBAN helpers (``acalculate_check_digits``, ``avalidate_iban``,
``agenerate_*``) are thin coroutines that call their sync siblings
directly. They exist so async code can ``await`` them without ceremony.

Determinism
-----------

SmartFaker uses the global :mod:`random` module under the hood. Seed it
yourself if you need reproducible output::

    import random
    from smartfaker import Faker

    random.seed(1234)
    faker = Faker()
    print(faker.iban("DE")["iban"])
