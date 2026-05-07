Seed a Database
===============

Populate a SQLAlchemy database with fake users for testing.

.. code-block:: python

    from sqlalchemy import Column, Integer, String, create_engine
    from sqlalchemy.orm import declarative_base, Session

    from smartfaker import Faker

    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        city = Column(String, nullable=False)
        country = Column(String(2), nullable=False)
        iban = Column(String(34))

    engine = create_engine("sqlite:///demo.db")
    Base.metadata.create_all(engine)

    faker = Faker()

    iban_supported = {c["country_code"] for c in faker.iban_countries()}

    with Session(engine) as session:
        for code in ["us", "gb", "de", "fr"]:
            upper = code.upper()
            for addr in faker.address(code, amount=50):
                iban = faker.iban(upper)["iban"] if upper in iban_supported else None
                session.add(User(
                    name=addr.get("person_name", "Anon"),
                    city=addr.get("city", "?"),
                    country=upper,
                    iban=iban,
                ))
        session.commit()

    print("Seeded 200 users.")
