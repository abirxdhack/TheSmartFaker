## SmartFaker

A powerful Python library for generating fake addresses, supporting up to 103 countries. Ideal for bots, MTProto API frameworks, and Python scripts.

### Installation
pip install smartfaker

### Usage

#### Basic Asyncio Example
```python
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
	
```

	
#### Basic Pyrofork Example	

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
    
    await send_countries_page(client, chat_id, 0, page_data[chat_id])  # Use 0 for initial message_id

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
        response += f"   - Code: {country['country_code']}\n"
        response += f"   - Flag: {flag}\n\n"
    
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
        return  # No edit for initial send
    
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
	