from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    set_description = State()
    set_phone = State()
    set_address = State()
    create_order = State()


class OperatorStates(StatesGroup):
    set_name = State()
    set_spec = State()
    accepted_order = State()
    wait_reason = State()


class AdminStates(StatesGroup):
    invite_operator = State()
