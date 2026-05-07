CLI Tool
========

A self-contained command-line script that prints a fake address or IBAN.

.. code-block:: python

    # smartfaker_cli.py
    import argparse
    import json
    import sys

    from smartfaker import Faker

    def main(argv=None):
        parser = argparse.ArgumentParser(prog="smartfaker", description="Generate fake addresses & IBANs.")
        sub = parser.add_subparsers(dest="cmd", required=True)

        p_addr = sub.add_parser("address", help="Generate fake address(es)")
        p_addr.add_argument("country")
        p_addr.add_argument("-n", "--amount", type=int, default=1)
        p_addr.add_argument("-f", "--field", action="append", help="Field to keep (repeat).")

        p_iban = sub.add_parser("iban", help="Generate fake IBAN(s)")
        p_iban.add_argument("country")
        p_iban.add_argument("-n", "--amount", type=int, default=1)

        sub.add_parser("countries", help="List supported address countries")
        sub.add_parser("iban-countries", help="List supported IBAN countries")

        args = parser.parse_args(argv)
        faker = Faker()

        if args.cmd == "address":
            result = faker.address(args.country, amount=args.amount, fields=args.field)
        elif args.cmd == "iban":
            result = faker.iban(args.country, amount=args.amount)
        elif args.cmd == "countries":
            result = faker.countries()
        elif args.cmd == "iban-countries":
            result = faker.iban_countries()
        else:  # pragma: no cover
            parser.error("unknown command")

        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")

    if __name__ == "__main__":
        main()

Usage::

    python smartfaker_cli.py address us -n 3
    python smartfaker_cli.py iban DE -n 5
    python smartfaker_cli.py countries
