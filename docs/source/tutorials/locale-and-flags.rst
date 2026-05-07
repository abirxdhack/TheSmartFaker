Locale & Country Flags
======================

Locale-prefixed names
---------------------

Pass ``locale="en_GB"`` (or any string) to prefix the ``person_name`` field
of generated addresses. This is useful when you want to track which locale
a row was seeded from inside test fixtures.

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    addr = faker.address("gb", locale="en_GB")
    assert addr["person_name"].startswith("en_GB_")

Country flags
-------------

Every address dict includes a ``country_flag`` field carrying the
regional-indicator emoji for the requested country.

.. code-block:: python

    faker.address("jp")["country_flag"]   # "🇯🇵"
    faker.address("br")["country_flag"]   # "🇧🇷"

You can also derive the flag from a country code without generating an
address by using the helper directly::

    from smartfaker.fake import _country_flag
    _country_flag("US")  # "🇺🇸"

(The helper is internal and may change between releases — prefer reading
``country_flag`` from a generated dict in production code.)
