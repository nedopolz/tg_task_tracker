from aiogram import Dispatcher

from .my_id import MyIdMiddleware
from .throttling import ThrottlingMiddleware
from src.data.config import admins


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(MyIdMiddleware(admins))
