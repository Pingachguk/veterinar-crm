from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from .dialogs import get_dialog

async def setup(dp: Dispatcher):
    pass
    # registry = DialogRegistry(dp)
    # registry.register(get_dialog())
    # registry.register(cart_dialog())

