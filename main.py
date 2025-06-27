import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import calc
import config

# Объект бота
bot = Bot(token=config.token)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    await message.reply("Калькулятор дайсов. Пока не допиленный.\n"
                        "Понимает простые математические операции (+ - * /) "
                        "и скобочки.\nБросок кубов производится в формате '2d6',"
                        "где '2' - это кол-во дайсов, а '6' - кол-во граней "
                        "или в упрощенном формате 'd20'")


# Хэндлер на команду /roll и /r
@dp.message(Command("roll", "r"))
async def cmd_roll(message: types.Message):
    try:
        await message.reply(calc.calculate(message.text))
    except Exception as err:
        return err


# Хендлер на директ
@dp.message()
async def private(message: types.Message):
    if message.chat.type == 'private':
        try:
            await message.reply(calc.calculate(message.text))
        except Exception as err:
            return err


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
