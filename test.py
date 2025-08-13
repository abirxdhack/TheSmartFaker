import asyncio
from smartfaker import Faker

fake = Faker()

async def main():
    print("Enter country code (e.g., BD):")
    country_code = input().strip().upper()
    if not country_code:
        print("Country code is required.")
        return

    print("Enter amount (default 1):")
    amount_input = input().strip()
    amount = 1 if not amount_input else int(amount_input)

    try:
        addresses = await fake.address(country_code, amount)
        if amount == 1:
            print(addresses)
        else:
            for addr in addresses:
                print(addr)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())