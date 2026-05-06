import pytest

from smartfaker import Faker
from smartfaker.iban import calculate_check_digits, validate_iban


@pytest.fixture(scope="module")
def faker_instance() -> Faker:
    return Faker()


def test_countries_contains_common_entries(faker_instance: Faker) -> None:
    countries = faker_instance.countries()

    assert countries == sorted(countries, key=lambda item: item["country_name"])
    assert any(item["country_code"] == "US" for item in countries)
    assert any(item["country_code"] == "GB" for item in countries)


@pytest.mark.asyncio
async def test_address_returns_single_address_with_metadata(faker_instance: Faker) -> None:
    address = await faker_instance.address("us")

    assert address["country_code"] == "US"
    assert address["api_owner"] == "@ISmartCoder"
    assert address["api_updates"] == "t.me/TheSmartDev"
    assert address["country_flag"] == "🇺🇸"
    assert address["city"]


@pytest.mark.asyncio
async def test_address_filters_fields_without_leaking_original_values(faker_instance: Faker) -> None:
    address = await faker_instance.address("de", fields=["city", "postal_code"])

    assert address == {"city": address["city"], "postal_code": address["postal_code"]}


def test_address_sync_supports_locale_prefix(faker_instance: Faker) -> None:
    address = faker_instance.address_sync("gb", locale="en_GB")

    assert address["person_name"].startswith("en_GB_")
    assert address["country_flag"] == "🇬🇧"


@pytest.mark.asyncio
async def test_batch_addresses_skips_invalid_codes(faker_instance: Faker) -> None:
    addresses = await faker_instance.batch_addresses(["us", "xx", "gb"], amount=2)

    assert set(addresses) == {"US", "GB"}
    assert len(addresses["US"]) == 2
    assert len(addresses["GB"]) == 2


@pytest.mark.asyncio
async def test_address_rejects_unknown_country(faker_instance: Faker) -> None:
    with pytest.raises(ValueError, match="Invalid country code"):
        await faker_instance.address("zz")


@pytest.mark.asyncio
async def test_iban_generation_returns_valid_payload(faker_instance: Faker) -> None:
    iban = await faker_instance.iban("DE")

    assert iban["country"] == "DE"
    assert iban["valid"] is True
    assert iban["length"] == len(iban["iban"])
    assert iban["details"]["bank_code"]
    assert await validate_iban(iban["iban"]) is True


def test_iban_sync_can_generate_multiple_results(faker_instance: Faker) -> None:
    ibans = faker_instance.iban_sync("GB", amount=2)

    assert len(ibans) == 2
    assert all(item["country"] == "GB" for item in ibans)


def test_iban_countries_are_sorted_and_include_core_markets(faker_instance: Faker) -> None:
    countries = faker_instance.iban_countries()

    assert countries == sorted(countries, key=lambda item: item["country_name"])
    assert any(item["country_code"] == "DE" for item in countries)
    assert any(item["country_code"] == "GB" for item in countries)


@pytest.mark.asyncio
async def test_calculate_check_digits_produces_known_german_example() -> None:
    check_digits = await calculate_check_digits("DE", "370400440532013000")

    assert check_digits == "89"


@pytest.mark.asyncio
async def test_validate_iban_rejects_bad_value() -> None:
    assert await validate_iban("DE89370400440532013001") is False