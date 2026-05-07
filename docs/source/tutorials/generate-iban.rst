Generate an IBAN
================

The :meth:`~smartfaker.Faker.iban` method generates one or more
structurally valid IBAN numbers for a given country.

Single IBAN
-----------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()
    iban = faker.iban("DE")
    print(iban["iban"])
    print(iban["details"]["bank_code"], iban["details"]["account_number"])

Multiple IBANs
--------------

.. code-block:: python

    ibans = faker.iban("GB", amount=10)
    for entry in ibans:
        print(entry["iban"])

Async
-----

.. code-block:: python

    import asyncio

    async def main():
        iban = await faker.aiban("FR")
        print(iban["iban"])

    asyncio.run(main())

Validation
----------

Every generated IBAN is re-validated with MOD-97 before being returned. If
generation produces an invalid value SmartFaker raises :class:`ValueError`.

To validate an arbitrary IBAN string yourself::

    from smartfaker.iban import validate_iban

    validate_iban("DE89370400440532013000")  # True

See :doc:`../advanced/iban-algorithm` for the full algorithm walk-through.
