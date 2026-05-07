CSV Export
==========

Generate fake addresses and dump them to a CSV file.

.. code-block:: python

    import csv
    from smartfaker import Faker

    FIELDS = ["person_name", "city", "street", "postal_code", "country_code"]

    faker = Faker()

    with open("seed_addresses.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for code in ["us", "gb", "de", "fr", "jp"]:
            for addr in faker.address(code, amount=200):
                writer.writerow(addr)

    print("Wrote seed_addresses.csv")

Async variant
-------------

For very large dumps, generate concurrently with the async API:

.. code-block:: python

    import asyncio, csv
    from smartfaker import Faker

    faker = Faker()

    async def make(code):
        return code, await faker.aaddress(code, amount=500)

    async def main():
        codes = ["us", "gb", "de", "fr", "jp", "br", "in", "au"]
        results = await asyncio.gather(*(make(c) for c in codes))
        with open("seed_addresses_async.csv", "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["country", "city"])
            writer.writeheader()
            for code, rows in results:
                for row in rows:
                    writer.writerow({"country": code, "city": row.get("city", "")})

    asyncio.run(main())
