Quickstart
==========

Install SmartFaker from PyPI::

    pip install smartfaker

Generate a fake address
-----------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    # Async usage
    import asyncio
    addr = asyncio.run(faker.address("us"))
    print(addr)

    # Sync usage
    addr = faker.address_sync("gb")
    print(addr)

Generate a fake IBAN
--------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    iban = faker.iban_sync("DE")
    print(iban["iban"])        # e.g. DE12500105170648489890
    print(iban["details"])     # parsed fields

List supported countries
------------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    # Address countries
    for c in faker.countries():
        print(c["country_code"], c["country_name"])

    # IBAN countries
    for c in faker.iban_countries():
        print(c["country_code"], c["country_name"])

Batch generation
----------------

.. code-block:: python

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    # Multiple countries at once
    results = asyncio.run(faker.batch_addresses(["us", "gb", "de", "fr"]))
    for code, addr in results.items():
        print(code, addr["city"])

    # Multiple addresses per country
    addrs = asyncio.run(faker.address("us", amount=5))
