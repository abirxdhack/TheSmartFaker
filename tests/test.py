"""SmartFaker test suite covering both sync and async APIs."""

import pytest

from smartfaker import Faker, __version__
from smartfaker.iban import (
    acalculate_check_digits,
    avalidate_iban,
    calculate_check_digits,
    validate_iban,
)


@pytest.fixture(scope="module")
def faker_instance() -> Faker:
    return Faker()


def test_version_is_string():
    assert isinstance(__version__, str) and __version__


def test_countries_sorted_and_contains_core(faker_instance: Faker) -> None:
    countries = faker_instance.countries()
    assert countries == sorted(countries, key=lambda item: item["country_name"])
    assert any(item["country_code"] == "US" for item in countries)
    assert any(item["country_code"] == "GB" for item in countries)


def test_address_sync_returns_metadata(faker_instance: Faker) -> None:
    address = faker_instance.address("us")
    assert address["country_code"] == "US"
    assert address["api_owner"] == "@ISmartCoder"
    assert address["api_updates"] == "t.me/TheSmartDev"
    assert address["country_flag"] == "🇺🇸"
    assert address["city"]


def test_address_sync_field_filter(faker_instance: Faker) -> None:
    address = faker_instance.address("de", fields=["city", "postal_code"])
    assert set(address.keys()) <= {"city", "postal_code"}


def test_address_sync_locale(faker_instance: Faker) -> None:
    address = faker_instance.address("gb", locale="en_GB")
    assert address["person_name"].startswith("en_GB_")
    assert address["country_flag"] == "🇬🇧"


def test_address_amount(faker_instance: Faker) -> None:
    addresses = faker_instance.address("fr", amount=3)
    assert isinstance(addresses, list)
    assert len(addresses) == 3


def test_batch_addresses_skips_invalid(faker_instance: Faker) -> None:
    addresses = faker_instance.batch_addresses(["us", "xx", "gb"], amount=2)
    assert set(addresses) == {"US", "GB"}
    assert len(addresses["US"]) == 2


def test_address_rejects_unknown(faker_instance: Faker) -> None:
    with pytest.raises(ValueError, match="Invalid country code"):
        faker_instance.address("zz")


def test_iban_sync_payload(faker_instance: Faker) -> None:
    iban = faker_instance.iban("DE")
    assert iban["country"] == "DE"
    assert iban["valid"] is True
    assert iban["length"] == len(iban["iban"])
    assert iban["details"]["bank_code"]
    assert validate_iban(iban["iban"]) is True


def test_iban_sync_amount(faker_instance: Faker) -> None:
    ibans = faker_instance.iban("GB", amount=2)
    assert len(ibans) == 2
    assert all(item["country"] == "GB" for item in ibans)


def test_iban_countries_sorted(faker_instance: Faker) -> None:
    countries = faker_instance.iban_countries()
    assert countries == sorted(countries, key=lambda item: item["country_name"])
    assert any(item["country_code"] == "DE" for item in countries)


def test_calculate_check_digits_known_german():
    assert calculate_check_digits("DE", "370400440532013000") == "89"


def test_validate_iban_rejects_bad():
    assert validate_iban("DE89370400440532013001") is False


# -------- async API --------


@pytest.mark.asyncio
async def test_aaddress_returns_metadata(faker_instance: Faker) -> None:
    address = await faker_instance.aaddress("us")
    assert address["country_code"] == "US"
    assert address["country_flag"] == "🇺🇸"


@pytest.mark.asyncio
async def test_aiban_payload(faker_instance: Faker) -> None:
    iban = await faker_instance.aiban("FR")
    assert iban["country"] == "FR"
    assert iban["valid"] is True
    assert await avalidate_iban(iban["iban"]) is True


@pytest.mark.asyncio
async def test_abatch_addresses(faker_instance: Faker) -> None:
    res = await faker_instance.abatch_addresses(["us", "gb"], amount=2)
    assert set(res) == {"US", "GB"}


@pytest.mark.asyncio
async def test_acalculate_check_digits():
    assert await acalculate_check_digits("DE", "370400440532013000") == "89"
