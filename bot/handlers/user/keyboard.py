from aiogram import types


def start_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Создать заявку"))
    return markup