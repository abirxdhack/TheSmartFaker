Telegram Bot Integration
========================

Build a Telegram bot that returns a random address or IBAN on demand.
Example uses :mod:`aiogram`, but the same pattern works with
``python-telegram-bot``, ``pyrogram``, or any other framework.

.. code-block:: python

    import asyncio
    from aiogram import Bot, Dispatcher, F
    from aiogram.types import Message
    from smartfaker import Faker

    BOT_TOKEN = "..."

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    faker = Faker()

    @dp.message(F.text.startswith("/addr "))
    async def cmd_addr(msg: Message) -> None:
        country = msg.text.split(maxsplit=1)[1].strip()
        try:
            addr = await faker.aaddress(country)
        except ValueError as exc:
            await msg.answer(f"❌ {exc}")
            return
        await msg.answer(
            f"{addr['country_flag']} {addr.get('city','?')}\n"
            f"{addr.get('street','')}\n"
            f"{addr.get('zip', addr.get('postal_code',''))}"
        )

    @dp.message(F.text.startswith("/iban "))
    async def cmd_iban(msg: Message) -> None:
        country = msg.text.split(maxsplit=1)[1].strip().upper()
        try:
            iban = await faker.aiban(country)
        except ValueError as exc:
            await msg.answer(f"❌ {exc}")
            return
        await msg.answer(f"`{iban['iban']}`", parse_mode="MarkdownV2")

    async def main():
        await dp.start_polling(bot)

    if __name__ == "__main__":
        asyncio.run(main())

Notes
-----

- ``Faker()`` is created **once** at module import.
- All handlers use the ``a*`` API so polling stays non-blocking.
