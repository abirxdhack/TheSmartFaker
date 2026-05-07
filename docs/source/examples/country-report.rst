Country Coverage Report
=======================

Generate a coverage matrix showing which countries support address
generation, IBAN generation, or both.

.. code-block:: python

    from smartfaker import Faker

    faker = Faker()

    address_codes = {c["country_code"] for c in faker.countries()}
    iban_codes = {c["country_code"] for c in faker.iban_countries()}

    both = address_codes & iban_codes
    only_address = address_codes - iban_codes
    only_iban = iban_codes - address_codes

    print(f"Address-only: {len(only_address)}")
    print(f"IBAN-only:    {len(only_iban)}")
    print(f"Both:         {len(both)}")
    print(f"Total unique: {len(address_codes | iban_codes)}")

CSV report
----------

.. code-block:: python

    import csv
    from smartfaker import Faker

    faker = Faker()
    address_codes = {c["country_code"] for c in faker.countries()}
    iban_codes = {c["country_code"] for c in faker.iban_countries()}

    with open("coverage.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["country_code", "address", "iban"])
        for code in sorted(address_codes | iban_codes):
            writer.writerow([code, code in address_codes, code in iban_codes])
