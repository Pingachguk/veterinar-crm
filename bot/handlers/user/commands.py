import json
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from .keyboard import start_keyboard
from states.user.states import OperatorStates
from settings.config import API_ORDERS, API_ORDER, rights

import requests


async def start(message: types.Message, state: FSMContext):
    # markup = start_keyboard(message.from_user.id)
    await message.answer(rights)

async def check_id(message: types.Message):
    await message.answer(message.chat.id)

async def clear_state(message: types.Message, state: FSMContext):
    await state.reset_state(True)
    await message.answer("Состояния очищены")

async def become_operator(message: types.Message, state: FSMContext):
    markup = start_keyboard(message.from_user.id)
    await message.answer("Используйте клавиатуру для подачи заявки.", reply_markup=markup)

async def become_doctor(message: types.Message, state: FSMContext):
    arg_com = message.get_args()
    if True:
        await state.update_data(doctor={"user_id": message.from_user.id})
        await message.answer("Введите Ваше имя: ")
        await state.set_state(OperatorStates.set_name)

async def accept_order(message: types.Message, state: FSMContext):
    arg_com = message.get_args()
    if not arg_com:
        return
    order: list = json.loads(requests.get(API_ORDER+arg_com+"/").content)
    if len(order) < 1:
        await message.answer("Некорректный номер заявки.")
        return
    order["is_accept"] = True
    requests.put(url=API_ORDER+arg_com+"/", data=order)
    await message.answer("Вы приняли заявку #"+arg_com)

async def finish_order(message: types.Message, state: FSMContext):
    arg_com = message.get_args()
    if not arg_com:
        await message.answer("Укажите номер заявки")
        return


async def send_rights(message:types.Message, state: FSMContext):
    await message.answer(rights)
