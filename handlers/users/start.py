from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from loader import dp
from utils.keyboards import menu


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("Что нужно сделать?", reply_markup=menu)


@dp.callback_query_handler(text_contains="back")
async def back(call: CallbackQuery):
    await call.message.edit_text("Что нужно сделать?", reply_markup=menu)
