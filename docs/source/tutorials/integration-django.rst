Django Integration
==================

Use SmartFaker inside Django views, management commands, factories, or
data-migration scripts.

A simple view
-------------

.. code-block:: python

    # app/views.py
    from django.http import JsonResponse, HttpResponseBadRequest
    from smartfaker import Faker

    faker = Faker()

    def address_view(request, country):
        try:
            return JsonResponse(faker.address(country), safe=False)
        except ValueError as exc:
            return HttpResponseBadRequest(str(exc))

    def iban_view(request, country):
        try:
            return JsonResponse(faker.iban(country))
        except ValueError as exc:
            return HttpResponseBadRequest(str(exc))

URL wiring::

    # app/urls.py
    from django.urls import path
    from .views import address_view, iban_view

    urlpatterns = [
        path("address/<str:country>/", address_view),
        path("iban/<str:country>/", iban_view),
    ]

Seeding fixtures
----------------

.. code-block:: python

    # app/management/commands/seed_users.py
    from django.core.management.base import BaseCommand
    from smartfaker import Faker
    from app.models import User

    class Command(BaseCommand):
        help = "Seed demo users with fake addresses"

        def handle(self, *args, **options):
            faker = Faker()
            for code in ["us", "gb", "de", "fr"]:
                for addr in faker.address(code, amount=25):
                    User.objects.create(
                        name=addr.get("person_name", "Anon"),
                        city=addr.get("city", ""),
                        country=code.upper(),
                    )
            self.stdout.write(self.style.SUCCESS("Done."))

For Django's async views, swap to the ``a*`` API exactly as in the FastAPI
example.
