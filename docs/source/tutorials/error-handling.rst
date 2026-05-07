Error Handling
==============

SmartFaker raises :class:`ValueError` for every invalid input.

Address errors
--------------

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    try:
        faker.address("zz")
    except ValueError as exc:
        print("address failed:", exc)

Cases that raise :class:`ValueError`:

- empty country code
- unknown country code (no bundled data)
- country bucket present but empty

IBAN errors
-----------

.. code-block:: python

    try:
        faker.iban("XX")
    except ValueError as exc:
        print("iban failed:", exc)

Cases that raise :class:`ValueError`:

- empty country code
- country code not in :data:`smartfaker.iban.COUNTRY_GENERATORS`
- generated IBAN failed length or MOD-97 self-check (defensive — should not
  happen with the bundled generators, but is checked anyway)

Batch behaviour
---------------

:meth:`~smartfaker.Faker.batch_addresses` and
:meth:`~smartfaker.Faker.abatch_addresses` are deliberately tolerant —
unknown country codes are *skipped* and omitted from the result mapping
rather than raising. Validate the returned keys instead:

.. code-block:: python

    res = faker.batch_addresses(["us", "xx", "gb"])
    assert set(res) == {"US", "GB"}
