from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import CallbackQuery

from src.loader import dp, controller
from src.utils.API.baseAPI import ToDoItem, ColorEnum
from src.utils.keyboards import create_active_to_do_keyboard, color_keyboard, menu


@dp.callback_query_handler(text_contains="list_all")
async def list_all(call: CallbackQuery):
    active_to_do = await controller.list_tasks()
    keyboard = create_active_to_do_keyboard(active_to_do)
    await call.message.edit_text(text="На сегодня:")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text_contains="sync")
async def sync(call: CallbackQuery):
    await controller.sync_all()
    await call.message.edit_text("Синхронизация прошла успешно", reply_markup=menu)


@dp.message_handler()
async def add_todo(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.update_data({"text": message.text})
    await message.answer(text="Какой цвет у этой задачи?", reply_markup=color_keyboard)


@dp.callback_query_handler(text_contains="color", state="*")
async def choose_color(call: CallbackQuery, state: FSMContext):
    color = call.data.split(":")[1]
    state_data = await state.get_data()
    task_text = state_data.get("text")
    todo = ToDoItem(name=task_text, color=ColorEnum(color), is_done=False)
    await controller.add(todo)
    await call.message.edit_text("Задача добавлена", reply_markup=menu)


@dp.callback_query_handler(text_contains="task_name", state="*")
async def mark_as_done(call: CallbackQuery, state: FSMContext):
    task_name = call.data.split(":")[1]
    await controller.mark_as_done(task_name)
    await call.answer("Молодец")
    active_to_do = await controller.list_tasks()
    keyboard = create_active_to_do_keyboard(active_to_do)
    await call.message.edit_reply_markup(reply_markup=keyboard)
