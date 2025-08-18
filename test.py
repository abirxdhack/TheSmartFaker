#Copyright @ISmartCoder
#Updates Channel @TheSmartDev
import asyncio
from smartfaker import Faker

fake = Faker()

async def main():
    """Main function to provide a menu-driven interface for generating fake addresses and IBANs."""
    while True:
        print("\nSelect an option:")
        print("1. Generate Fake Address Based On Code")
        print("2. Get Available Fake Address Countries")
        print("3. Generate Fake Iban Based On Code")
        print("4. Get Available Fake Ibans Countries")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            print("Enter country code (e.g., DE):")
            country_code = input().strip().upper()
            if not country_code:
                print("Country code is required.")
                continue
            print("Enter amount (default 1):")
            amount_input = input().strip()
            amount = 1 if not amount_input else int(amount_input)
            try:
                addresses = await fake.address(country_code, amount)
                print("Addresses:")
                if amount == 1:
                    print(addresses)
                else:
                    for addr in addresses:
                        print(addr)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            countries = fake.countries()
            print("Available Fake Address Countries:")
            for country in countries:
                print(f"{country['country_code']}: {country['country_name']}")
        elif choice == "3":
            print("Enter country code (e.g., DE):")
            country_code = input().strip().upper()
            if not country_code:
                print("Country code is required.")
                continue
            print("Enter amount (default 1):")
            amount_input = input().strip()
            amount = 1 if not amount_input else int(amount_input)
            try:
                ibans = await fake.iban(country_code, amount)
                print("IBANs:")
                if amount == 1:
                    print(ibans)
                else:
                    for iban in ibans:
                        print(iban)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            countries = fake.iban_countries()
            print("Available Fake IBAN Countries:")
            for country in countries:
                print(f"{country['country_code']}: {country['country_name']}")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    asyncio.run(main())
