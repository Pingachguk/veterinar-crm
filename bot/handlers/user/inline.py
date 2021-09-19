from aiogram import types
from aiogram.utils.callback_data import CallbackData


order_cb = CallbackData("btn", "order_id", "doctor_id", "input", "client_id")
async def get_markup(order_id, doctor_id, client_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Принять", callback_data=order_cb.new(order_id=order_id, doctor_id=doctor_id, client_id=client_id, input="accept")
    )) 
    markup.add(types.InlineKeyboardButton(
        "Отменить", callback_data=order_cb.new(order_id=order_id, doctor_id=doctor_id, client_id=client_id, input="cancel")
    )) 
    return markup

async def get_markup_2(order_id, doctor_id, client_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Выполнить", callback_data=order_cb.new(order_id=order_id, doctor_id=doctor_id, client_id=client_id, input="ready")
    ))
    markup.add(types.InlineKeyboardButton(
        "Отменить", callback_data=order_cb.new(order_id=order_id, doctor_id=doctor_id, client_id=client_id, input="cancel2")
    ))  
    return markup
