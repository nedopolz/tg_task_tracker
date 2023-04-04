import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class MyIdMiddleware(BaseMiddleware):
    """
    Simple middleware to cancel all requests not from my id
    """

    def __init__(self, trusted_ids: list):
        self.trusted_ids = trusted_ids
        super(MyIdMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if str(message.from_user.id) not in self.trusted_ids:
            raise CancelHandler()
