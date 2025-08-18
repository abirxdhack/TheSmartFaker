# SmartFaker

A powerful asynchronous Python library for generating fake addresses and IBANs, supporting up to 181 countries for addresses and 50+ countries for IBANs. Ideal for bots, MTProto API frameworks, and Python scripts.

---

## What's New in Version 3.25.1
- **Added IBAN Generation**: Generate valid IBANs for over 53 countries with detailed breakdowns (e.g., bank code, account number).
- Improved metadata for proper author display in PyPI.
- Fixed typo in description ("Asyncrhonous" to "Asynchronous").

---

## Installation

Install SmartFaker via pip:

```bash
pip install smartfaker
```

---

## Usage

SmartFaker supports both asynchronous and synchronous generation of fake addresses and IBANs. Below are examples for using the library in different contexts.

### Basic Asyncio Example

This example demonstrates the menu-driven interface for generating addresses, listing available address countries, generating IBANs, and listing available IBAN countries.

```python
import asyncio
from smartfaker import Faker

fake = Faker()

async def main():
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
```

### Basic Pyrofork Example

This example shows how to integrate SmartFaker with a Pyrofork bot to generate fake addresses via Telegram commands.

```python
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from smartfaker import Faker
import pycountry

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

COMMAND_PREFIX = ["/", ",", ".", "!", "#"]

app = Client(
    "my_bot",
    api_id=YOUR_API_ID,
    api_hash="YOUR_API_HASH",
    bot_token="YOUR_BOT_TOKEN"
)

fake = Faker()
page_data = {}

def get_flag(country_code):
    try:
        return ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())
    except Exception:
        return "🏚"

@app.on_message(filters.command("start", prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
async def start_handler(client: Client, message: Message):
    welcome_text = (
        "**Welcome to SmartFaker Bot! 🚀**\n"
        "**━━━━━━━━━━━━━**\n"
        "Generate fake addresses easily!\n"
        "Use **/fake <code>** for an address (e.g., /fake BD).\n"
        "Use **/countries** to list available countries.\n"
        "**━━━━━━━━━━━━━**\n"
        "Powered by @ISmartCoder | Updates: t.me/TheSmartDev"
    )
    await client.send_message(message.chat.id, welcome_text, parse_mode=ParseMode.MARKDOWN)

@app.on_message(filters.command(["fake", "rnd"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
async def fake_handler(client: Client, message: Message):
    if len(message.command) <= 1:
        await client.send_message(message.chat.id, "**❌ Please Provide A Country Code**", parse_mode=ParseMode.MARKDOWN)
        LOGGER.warning(f"Invalid command format: {message.text}")
        return
    
    country_code = message.command[1].upper()
    if country_code == "UK":
        country_code = "GB"
    
    generating_message = await client.send_message(message.chat.id, "**Generating Fake Address...**", parse_mode=ParseMode.MARKDOWN)
    
    try:
        data = await fake.address(country_code)
        flag_emoji = data['country_flag']
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Copy Postal Code", callback_data=f"copy:{data['postal_code']}")]
        ])
        await generating_message.edit_text(
            f"**Address for {data['country']} {flag_emoji}**\n"
            f"**━━━━━━━━━━━━━**\n"
            f"**- Street :** `{data['street_address']}`\n"
            f"**- Full Name :** `{data['person_name']}`\n"
            f"**- City/Town/Village :** `{data['city']}`\n"
            f"**- Gender :** `{data['gender']}`\n"
            f"**- Postal Code :** `{data['postal_code']}`\n"
            f"**- Phone Number :** `{data['phone_number']}`\n"
            f"**- Country :** `{data['country']}`\n"
            f"**━━━━━━━━━━━━━**\n"
            f"**Click Below Button For Code 👇**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
        LOGGER.info(f"Sent fake address for {country_code} in chat {message.chat.id}")
    except ValueError as e:
        LOGGER.error(f"Fake address error for country '{country_code}': {e}")
        await generating_message.edit_text("**❌ Sorry, Fake Address Generator Failed**", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        LOGGER.error(f"Fake address error for country '{country_code}': {e}")
        await generating_message.edit_text("**❌ Sorry, Fake Address Generator Failed**", parse_mode=ParseMode.MARKDOWN)

@app.on_message(filters.command("countries", prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
async def countries_handler(client: Client, message: Message):
    chat_id = message.chat.id
    page_data[chat_id] = page_data.get(chat_id, 0)
    
    countries = fake.countries()
    total_pages = (len(countries) + 9) // 10
    if not countries or total_pages == 0:
        await client.send_message(message.chat.id, "No countries available.")
        return
    
    await send_countries_page(client, chat_id, 0, page_data[chat_id]) # Use 0 for initial message_id

async def send_countries_page(client: Client, chat_id: int, message_id: int, page: int):
    countries = fake.countries()
    total_pages = (len(countries) + 9) // 10
    start_idx = page * 10
    end_idx = min(start_idx + 10, len(countries))
    current_countries = countries[start_idx:end_idx]
    
    response = "**Available Countries (Page {}/{}):**\n\n".format(page + 1, total_pages)
    for i, country in enumerate(current_countries, start=start_idx + 1):
        flag = get_flag(country['country_code'])
        response += f"**{i}. {country['country_name']}**\n"
        response += f" - Code: {country['country_code']}\n"
        response += f" - Flag: {flag}\n\n"
    
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    if page > 0:
        row.append(InlineKeyboardButton("Previous", callback_data=f"prev:{page}:{chat_id}"))
    if page < total_pages - 1:
        row.append(InlineKeyboardButton("Next", callback_data=f"next:{page}:{chat_id}"))
    if row:
        markup.inline_keyboard.append(row)
    
    if message_id == 0:
        sent_msg = await client.send_message(chat_id, response, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
        return 
    
    await client.edit_message_text(chat_id, message_id, response, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

@app.on_callback_query(filters.regex(r"^(prev|next):(\d+):(\d+)$"))
async def pagination_handler(client: Client, callback_query):
    action, page_str, chat_id_str = callback_query.data.split(':')
    page = int(page_str)
    chat_id = int(chat_id_str)
    
    total_pages = (len(fake.countries()) + 9) // 10
    if action == "prev" and page > 0:
        page -= 1
    elif action == "next" and page < total_pages - 1:
        page += 1
    
    await send_countries_page(client, chat_id, callback_query.message.id, page)
    await callback_query.answer()

if __name__ == "__main__":
    app.run()
```

---

## Features
- **Asynchronous**: Built with `asyncio` for non-blocking performance.
- **Address Generation**: Supports fake addresses for 181 countries with details like street, city, postal code, and phone number.
- **IBAN Generation**: Generates valid IBANs for over 50 countries with detailed breakdowns (e.g., bank code, account number).
- **Country Listing**: Easily list supported countries for both addresses and IBANs.
- **Bot Integration**: Seamless integration with Telegram bots via Pyrofork or other MTProto frameworks.
- **Lightweight**: Minimal dependencies, requiring only `pycountry`.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request. For issues, report them on the [GitHub Issues](https://github.com/abirxdhack/TheSmartFaker/issues) page.

---

## License
SmartFaker is licensed under the [MIT License](LICENSE).

---

## Contact
- **Author**: @ISmartCoder
- **Email**: abrixdhackz.info.me@gmail.com
- **Updates Channel**: [t.me/TheSmartDev](https://t.me/TheSmartDev)
- **Documentation**: [SmartFaker Docs](https://abirxdhack.github.io/SmartFakerDocs)
