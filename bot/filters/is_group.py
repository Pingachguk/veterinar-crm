from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatType


class GroupFilter(BoundFilter):
    key = 'is_group'

    def __init__(self, is_group):
        self.is_group = is_group

    async def check(self, msg: Message):
        return msg.chat.type == ChatType.GROUP