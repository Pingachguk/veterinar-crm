from aiogram import Dispatcher
from .is_private import PrivateFilter
from .is_group import GroupFilter


async def setup(dp: Dispatcher):
    dp.filters_factory.bind(PrivateFilter)
    dp.filters_factory.bind(GroupFilter)