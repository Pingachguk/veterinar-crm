from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatType


class PrivateFilter(BoundFilter):
    key = 'is_private'

    def __init__(self, is_private):
        self.is_private = is_private

    async def check(self, msg: Message):
        return msg.chat.type == ChatType.PRIVATE