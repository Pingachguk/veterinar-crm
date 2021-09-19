from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from requests.models import Response
from states.user.states import UserStates, OperatorStates
from settings.config import API_DOCTORS, group_id
from datetime import datetime
from settings import config
from main import cache
from .inline import get_markup

import hashlib
import requests
import json


def to_hash(data):
    hash = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
    return hash

def get_order(order_list, order_id):
    for order in order_list:
        if (order["id"] == order_id):
            return order

def update_order(order_list, data):
    for order in order_list:
        if (order["id"] == data["id"]):
            order = data
    return order_list

async def set_item(item: str, message: types.Message, state: FSMContext):
    # Get order
    data: dict = await state.get_data()
    order_id = data["last_order"]
    order = get_order(data["order"], order_id)

    # Set item
    order[item] = message.text
    order_list = update_order(data["order"], order)
    await state.update_data(order=order_list)

async def set_order_dict(states: FSMContext):
    await states.update_data(order=[])

async def check_dict(state: FSMContext, key: str):
    data = await state.get_data()
    if key in data.keys():
        return True
    else: 
        return False

async def start_order(message: types.Message, state: FSMContext):
    if not (await check_dict(state, "order")):
        await set_order_dict(state)

    # Generate hash for order id
    order_id = to_hash(str(message.from_user.id)+str(datetime.now()))
    # Create new order
    order_list: list = (await state.get_data())["order"]
    order_list.append({"id": order_id})

    await state.update_data(order=order_list)
    await state.update_data(last_order=order_id)

    await state.set_state(UserStates.set_description)
    await message.answer("Опишите Ваш запрос:")

async def set_phone(message: types.Message, state: FSMContext):
    # Set description
    await set_item("description", message, state)

    await message.answer("Введите Ваш контактный номер телефона:")
    await state.set_state(UserStates.set_phone)

async def set_address(message: types.Message, state: FSMContext):
    # Set phone
    await set_item("phone", message, state)

    await message.answer("Введите Ваш адрес:")
    await state.set_state(UserStates.set_address)

async def create_order(message: types.Message, state: FSMContext):
    # Set address
    await set_item("address", message, state)

    # Set address order
    await message.answer("Ваш запрос отправлен нашим операторам. В ближайшее время мы уведомим Вас.")
    await state.reset_state(False)

    # Create order text
    data = await state.get_data()
    order = get_order(data["order"], data["last_order"])

    # Post order data on API
    post_data = {
        "user_id": message.from_user.id,
        "order_id": order["id"],
        "description": order["description"],
        "phone": order["phone"],
        "address": order["address"],
        "is_accept": False
    }
    response = json.loads(requests.post(url=config.API_ORDERS, data=post_data).content)
    order_text = "Заявка #{id}\n\n<b>Адрес:</b> {address}\n<b>Описание:</b>\n{text}\n<b>Номер:</b> {phone}".format(id=response["id"], address=order["address"], text=order["description"], phone=order["phone"])

    # Send to all doctors
    operators = json.loads(requests.get(config.API_DOCTORS).content)
    send_msg = []
    for operator in operators:
        markup: types.InlineKeyboardMarkup = await get_markup(response["id"], operator["user_id"], message.from_user.id)
        msg = await message.bot.send_message(operator["user_id"], order_text, reply_markup=markup)
        send_msg.append({operator["user_id"]: msg["message_id"]})
    
    cache.create_dict("order"+":"+str(response["id"]), send_msg)
    await message.bot.send_message(group_id, order_text)

#
# DOCTORS
# 

async def set_name(message: types.Message, state: FSMContext):
    doctor_data = (await state.get_data())["doctor"]
    doctor_data["name"] = message.text
    await state.update_data(doctor=doctor_data)
    await state.set_state(OperatorStates.set_spec)

    await message.answer("Введите Вашу специализацию")

async def set_spec(message: types.Message, state: FSMContext):
    doctor_data = (await state.get_data())["doctor"]
    doctor_data["spec"] = message.text
    await state.update_data(doctor=doctor_data)

    await message.answer("Ваш профиль готов к работе. Ожидайте заявки.")

    post_data = {
        "user_id": doctor_data["user_id"],
        "username": doctor_data["name"],
        "specialization": doctor_data["spec"],
    }
    requests.post(url=API_DOCTORS, data=post_data)

    await state.set_state(None)


async def send_reason(message: types.Message, state: FSMContext):
    client_id = (await state.get_data())["reason_to"]
    await message.bot.send_message(client_id, f"К сожалению, специалист отменил заявку.\n<b>Причина:</b>\n{message.text}")
    await state.reset_state(False)
