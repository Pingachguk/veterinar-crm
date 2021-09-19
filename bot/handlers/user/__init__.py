from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, Command, Text
from aiogram.types import ContentTypes
from . import commands, answers, callback_answer
from settings import config
from states.user.states import UserStates, OperatorStates
from .inline import order_cb


async def setup(dp: Dispatcher):
    # Clear states
    dp.register_message_handler(commands.clear_state, Command("reset"), state="*", is_private=True)

    # Create order
    dp.register_message_handler(answers.start_order, Text(config.keyboard["create"]), is_private=True)
    dp.register_message_handler(answers.set_phone, is_private=True, state=UserStates.set_description)
    dp.register_message_handler(answers.set_address, is_private=True, state=UserStates.set_phone)
    dp.register_message_handler(answers.create_order, is_private=True, state=UserStates.set_address)

    # Become doctors
    dp.register_message_handler(answers.set_name, is_private=True, state=OperatorStates.set_name)
    dp.register_message_handler(answers.set_spec, is_private=True, state=OperatorStates.set_spec)

    # Doctors handler
    dp.register_message_handler(answers.send_reason, is_private=True, state=OperatorStates.wait_reason)

    # Callback
    dp.register_callback_query_handler(callback_answer.order, order_cb.filter(), state="*")

    # Commands
    dp.register_message_handler(commands.accept_order, Command('accept'), state="*", is_private=True)
    dp.register_message_handler(commands.become_operator, Command('order'), state="*", is_private=True)
    dp.register_message_handler(commands.become_doctor, Command('register'), is_private=True, state=None)
    dp.register_message_handler(commands.start, CommandStart(), is_private=True)
    dp.register_message_handler(commands.finish_order, Command("finish"), is_private=True, state=OperatorStates.accepted_order)
    dp.register_message_handler(commands.send_rights, Command("help"), is_private=True, state="*")
    dp.register_message_handler(commands.check_id, Command("checkid"), is_group=True)

