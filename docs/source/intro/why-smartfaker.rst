Why SmartFaker
==============

There are dozens of fake-data libraries on PyPI. SmartFaker exists for a
specific niche the others don't fully cover.

No network, ever
----------------

The bundled JSON data set means SmartFaker is safe in air-gapped CI, behind
restrictive corporate firewalls, in serverless cold-starts, and inside
Docker images that ban outbound traffic.

Sync **and** async, with identical contracts
--------------------------------------------

Other libraries either give you a sync API and ask you to wrap it in a
thread, or expose an async-only API that becomes painful in CLI scripts.
SmartFaker gives you both, with matching method signatures::

    faker.address("us")            # sync
    await faker.aaddress("us")     # async

Real per-country IBAN structure
-------------------------------

IBANs are not just random digits. SmartFaker implements 57 country-specific
BBAN layouts (Italian CIN, Belgian mod-97, French key, German bank codes,
US routing numbers, …) and re-validates every generated IBAN with the
ISO 13616 MOD-97 algorithm before returning it.

Tiny footprint
--------------

The wheel ships only the address JSON files, the IBAN module, the Faker
class and the bundled data — no native code, no large runtime
dependencies, no cloud SDKs.

Predictable shape, easy to mock
-------------------------------

Every response uses the same documented schema, so swapping SmartFaker for a
fixture in tests is trivial.
