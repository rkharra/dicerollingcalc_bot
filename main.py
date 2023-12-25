import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import calc
import config
import poker

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.token)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    await message.reply("Калькулятор дайсов. Пока не допиленный.\nПонимает простые математические операции (+ - * /) "
                        "и скобочки.\nБросок кубов производится в формате '2d6', где '2' - это кол-во дайсов, "
                        "а '6' - кол-во граней, или в упрощенном формате 'd20'")


# Хэндлер на команду /r
@dp.message(Command("r"))
async def cmd_start(message: types.Message):
    if len(message.text) > 3:
        formula = message.text[3:]
        try:
            result = str(calc.calculate(formula))
        except Exception as err:
            return err
        await message.reply(result)
    else:
        await message.reply("Huh?")
    print(f'{message.chat.first_name} input {message.text}')


# Хэндлер на команду /roll
@dp.message(Command("roll"))
async def cmd_start(message: types.Message):
    if len(message.text) > 6:
        formula = message.text[6:]
        try:
            result = str(calc.calculate(formula))
        except Exception as err:
            return err
        await message.reply(result)
    else:
        await message.reply("Huh?")
    print(f'{message.chat.first_name} input {message.text}')


# Хэндлер на команду /poker
@dp.message(Command("poker"))
async def cmd_start(message: types.Message):
    await message.reply(poker.poker())
    print(f'{message.chat.first_name} play Poker')


# Хендлер на директ
@dp.message()
async def private(message: types.Message):
    if message.chat.type == 'private':
        formula = message.text
        try:
            result = str(calc.calculate(formula))
        except Exception as err:
            return err
        await message.reply(result)
    print(f'{message.chat.first_name} input {message.text}')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
