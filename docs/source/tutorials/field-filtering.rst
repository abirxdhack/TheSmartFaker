Field Filtering
===============

By default, every address dictionary returned by SmartFaker contains every
field present in the bundled record plus the standard metadata keys. Pass a
``fields=[...]`` argument to keep only the keys you need.

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("de", fields=["city", "postal_code"])
    print(addr)
    # {"city": "Berlin", "postal_code": "10115"}

The metadata keys (``api_owner``, ``api_updates``, ``country_flag``) are
*also* removed when you pass ``fields=`` — the filter is exact.

Field filter applies per-record, so it works for ``amount > 1``:

.. code-block:: python

    addrs = faker.address("us", amount=5, fields=["city", "state"])
    for a in addrs:
        print(a["city"], a["state"])

Common fields
-------------

Available fields vary slightly between countries, but typical keys include:

- ``person_name``
- ``street``, ``street_address``
- ``city``, ``state`` or ``region``
- ``zip`` or ``postal_code``
- ``phone``, ``country_code``

Inspect the raw record once to discover the exact keys for a country::

    print(faker.address("us").keys())
