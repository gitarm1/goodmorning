import config
import logging
from sqlighter import SQLighter
from datetime import datetime
import asyncio


from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level = logging.INFO)


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

db = SQLighter('db.db')

@dp.message_handler(commands = ["admin"])
async def admin(message: types.Message):
    if message.from_user.id == 1076482828 and len(message.text) < 15:
        await message.answer("Վերջ✅")
        db.add_subscriber(message.text)

    elif message.from_user.id == 1076482828 and len(message.text) > 15:
        await message.answer("Վերջ✅")
        db.add_message(message.text)
    else:
        await message.answer("""Ես Ձեզ չեմ հասկանում(""")


@dp.message_handler(commands = ['start'])
async def echo(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        await message.answer("""Բարև 💛 Եթե դու որոշել ես, որ քո բարի լույսը պետք է սկսվի իմ հիշեցումներով, իմ խորհուրդներով, իմ մոտիվացիայով, իմ առաջարկած ֆիլմերով և գրքերով, ապա գրիր այս էջին, վճարիր 3000 դրամ և ես կդառնամ քո գիտելիքի, մոտիվացիայի աղբյուրը 300 օր շարունակ: Լինեմ ԲԱՐԻ ԼՈՒՅՍԴ 🌾☀️:

💖Գրանցվելու համար - @goodmorning_pay""")

    else:
        await message.answer("Դու արդեն գրանցված ես, ու ամեն օր ստանում ես քո մոտիվացիայի բաժինը☀️")

async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.now().strftime("%H:%M")
        print(now)
        if now == "12:00":
            for user in db.get_subscriptions():
                try:
                    await bot.send_message(user, db.get_messages()[0],
                                               disable_notification=False)

                except:
                    continue

            db.delete_first()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(60))
    executor.start_polling(dp)
