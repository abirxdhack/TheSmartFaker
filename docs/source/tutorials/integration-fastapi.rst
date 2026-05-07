FastAPI Integration
===================

A minimal FastAPI service that exposes SmartFaker through HTTP.

.. code-block:: python

    from fastapi import FastAPI, HTTPException
    from smartfaker import Faker

    app = FastAPI(title="SmartFaker API")
    faker = Faker()  # one shared instance

    @app.get("/address/{country}")
    async def get_address(country: str, amount: int = 1):
        try:
            return await faker.aaddress(country, amount=amount)
        except ValueError as exc:
            raise HTTPException(400, str(exc))

    @app.get("/iban/{country}")
    async def get_iban(country: str, amount: int = 1):
        try:
            return await faker.aiban(country, amount=amount)
        except ValueError as exc:
            raise HTTPException(400, str(exc))

    @app.get("/countries")
    def list_countries():
        return faker.countries()

    @app.get("/iban-countries")
    def list_iban_countries():
        return faker.iban_countries()

Run it::

    uvicorn main:app --reload

Test it::

    curl http://127.0.0.1:8000/address/us
    curl http://127.0.0.1:8000/iban/DE?amount=3

Notes
-----

- ``Faker()`` is created once at module import — never per request.
- Endpoints that touch the generator use the async ``a*`` methods so they
  cooperate with the event loop.
- The synchronous ``/countries`` endpoint is fine because it returns a
  small in-memory list.
