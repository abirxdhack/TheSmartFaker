Bulk IBAN Validator
===================

Validate a file full of IBANs against the bundled MOD-97 algorithm.

.. code-block:: python

    from smartfaker.iban import validate_iban

    def validate_file(path: str) -> dict:
        ok, bad = 0, 0
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                value = line.strip().replace(" ", "")
                if not value:
                    continue
                if validate_iban(value):
                    ok += 1
                else:
                    bad += 1
                    print("BAD", value)
        return {"valid": ok, "invalid": bad}

    print(validate_file("ibans.txt"))

Async / concurrent
------------------

If your input comes from an async source (HTTP body, queue, …) use the
async wrapper so the event loop stays free:

.. code-block:: python

    import asyncio
    from smartfaker.iban import avalidate_iban

    async def validate_stream(stream):
        async for value in stream:
            if not await avalidate_iban(value.strip()):
                print("BAD", value)

    asyncio.run(validate_stream(...))

Round-trip generation + validation
----------------------------------

.. code-block:: python

    from smartfaker import Faker
    from smartfaker.iban import validate_iban

    faker = Faker()

    for c in ("DE", "GB", "FR", "ES", "IT"):
        for entry in faker.iban(c, amount=100):
            assert validate_iban(entry["iban"]), entry["iban"]
    print("all generated IBANs validated")
