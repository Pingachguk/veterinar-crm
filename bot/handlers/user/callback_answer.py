from .inline import get_markup_2, get_markup
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from settings.config import API_ORDER
from states.user.states import OperatorStates

import requests
import json

def update_order(order_id, item, data):
    order = json.loads(requests.get(url=API_ORDER+order_id+"/").content)
    order[item] = data
    requests.put(url=API_ORDER+order_id+"/", data=order)

async def order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data["input"] == "accept":
        order = json.loads(requests.get(url=API_ORDER+callback_data["order_id"]+"/").content)
        if order["is_accept"]:
            await call.message.answer("Заявка уже принята другим специалистом")
            await call.message.delete_reply_markup()
            return
        if order["is_ready"]:
            await call.message.answer("Заявка уже обработана")
            await call.message.delete_reply_markup()
            return
        doctor = (await state.get_data())["doctor"]
        await call.bot.send_message(callback_data["client_id"], f"Вашу заявку принял наш специалист: {doctor['spec']} {doctor['name']}")
        await call.message.delete_reply_markup()
        await call.message.edit_reply_markup(await get_markup_2(callback_data["order_id"], call.from_user.id, callback_data["client_id"]))
        update_order(callback_data["order_id"], "is_accept", True)
        await state.set_state(OperatorStates.accepted_order)
    
    if callback_data["input"] == "cancel":
        await call.message.delete_reply_markup()
        await state.reset_state(False)

    if callback_data["input"] == "cancel2":
        # Set state wait answer
        await state.set_state(OperatorStates.wait_reason)
        await state.update_data(reason_to=callback_data["client_id"])
        await call.message.answer("Введите причину отмены")
        await call.message.edit_reply_markup(await get_markup(callback_data["order_id"], callback_data["doctor_id"], callback_data["client_id"]))
        update_order(callback_data["order_id"], "is_accept", False)
        
    if callback_data["input"] == "ready":
        await call.message.delete_reply_markup()
        update_order(callback_data["order_id"], "is_ready", True)
        await state.reset_state(False)
