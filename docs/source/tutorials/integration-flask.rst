Flask Integration
=================

Flask is synchronous by default, so use the synchronous SmartFaker methods
directly.

.. code-block:: python

    from flask import Flask, jsonify, abort
    from smartfaker import Faker

    app = Flask(__name__)
    faker = Faker()  # one shared instance

    @app.get("/address/<country>")
    def get_address(country):
        try:
            return jsonify(faker.address(country, amount=int(request.args.get("amount", 1))))
        except ValueError as exc:
            abort(400, str(exc))

    @app.get("/iban/<country>")
    def get_iban(country):
        try:
            return jsonify(faker.iban(country))
        except ValueError as exc:
            abort(400, str(exc))

    @app.get("/countries")
    def list_countries():
        return jsonify(faker.countries())

    if __name__ == "__main__":
        app.run(debug=True)

Run it::

    python app.py

If you use Flask's ``async`` view support (Flask 2+), feel free to use
``await faker.aaddress(...)`` instead — the choice is yours.
