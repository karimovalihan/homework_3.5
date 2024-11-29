import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram import types
from aiogram.filters import Command
from aiogram import *
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from app.db import *

token = os.environ.get('token')
print(token)

bot = Bot(token='7439688144:AAE9QvME9iXz3RRV3oPYn9mvrqYYVdrribE')
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class MyStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_receiver = State()

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    register_user(user_id)
    await message.answer("Я тг бот который проверяет сколько нащету у вас в банке и могу совершать переводы между счетами, используя конечный автомат")

@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("напишите команду в тг боте!")

@dp.message(Command("transfer"))
async def transfer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not has_account(user_id):
        await message.answer("Введите сумму перевода:")
        return
    await message.answer("Введите сумму перевода.")

@dp.message(Command("balance"))
async def balance(message: types.Message):
    user_id = message.from_user.id
    if has_account(user_id):
        await message.reply(f"Ваш текущий баланс: {balance} сомов.")
    else:
        await message.reply("У вас нет счета. Пожалуйста, зарегистрируйтесь для использования бота.")

# @dp.message(state=MyStates.waiting_for_amount)
# async def process_amount(message: types.Message, state: FSMContext):
#     try:
#         amount = float(message.text)
#         if amount <= 0:
#             await message.answer("Сумма перевода должна быть положительной.")
#             return

#         user_id = message.from_user.id
#         balance = get_balance(user_id)

#         if amount > balance:
#             await message.answer("На вашем счете недостаточно средств.")
#             return

#         await state.update_data(amount=amount)
#         await message.answer("Введите ID получателя или номер счета.")
#         await MyStates.waiting_for_receiver.set()
#     except ValueError:
#         await message.answer("Пожалуйста, введите правильную сумму.")

# @dp.message(state=MyStates.waiting_for_receiver)
# async def process_receiver(message: types.Message, state: FSMContext):
#     receiver_id = message.text
#     if not receiver_id.isdigit():
#         await message.answer("ID получателя должен быть числом. Попробуйте еще раз.")
#         return

#     receiver_id = int(receiver_id)
#     data = await state.get_data()
#     amount = data.get('amount')
#     sender_id = message.from_user.id

#     try:
#         update_balance(sender_id, -amount)
#         update_balance(receiver_id, amount)
#         add_transfer(sender_id, receiver_id, amount)

#         await message.answer(f"Перевод {amount} сом успешно выполнен!")
#     except Exception as e:
#         await message.answer(f"Ошибка при выполнении перевода: {e}")
#     finally:
#         await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())