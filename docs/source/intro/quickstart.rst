Quickstart
==========

Install SmartFaker from PyPI::

    pip install smartfaker

Generate a fake address
-----------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    import asyncio
    addr = asyncio.run(faker.address("us"))
    print(addr)

    addr = faker.address_sync("gb")
    print(addr)

Generate a fake IBAN
--------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    iban = faker.iban_sync("DE")
    print(iban["iban"])
    print(iban["details"])

List supported countries
------------------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    for c in faker.countries():
        print(c["country_code"], c["country_name"])

    for c in faker.iban_countries():
        print(c["country_code"], c["country_name"])

Batch generation
----------------

.. code-block:: python

    import asyncio
    from smartfaker import Faker

    faker = Faker()

    results = asyncio.run(faker.batch_addresses(["us", "gb", "de", "fr"]))
    for code, addr in results.items():
        print(code, addr["city"])

    addrs = asyncio.run(faker.address("us", amount=5))
