from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.API.baseAPI import ToDoItem, ColorEnum


def enum_to_color(enum: ColorEnum) -> str:
    match enum:
        case enum.RED:
            return "💥"
        case enum.BLUE:
            return "🐬"
        case enum.BROWN:
            return "💼"
        case enum.GREEN:
            return "🍀"
        case enum.YELLOW:
            return "🌝"


def get_short_name(full_name: str) -> str:
    if len(full_name) > 20:
        return full_name[:17] + "..."
    return full_name


def create_active_to_do_keyboard(todos: list[ToDoItem]) -> InlineKeyboardMarkup:
    base_text = "{} - {}\n"
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for todo in todos:
        short_name = get_short_name(todo.name)
        color = enum_to_color(todo.color)
        keyboard.add(InlineKeyboardButton(text=base_text.format(short_name, color),
                                          callback_data=f"task_name:{short_name}"))
    keyboard.add(back_button)
    return keyboard


color_keyboard = InlineKeyboardMarkup(
    row_width=5,
    resize_keyboard=True
)
color_keyboard.row(
    InlineKeyboardButton(text="🍀", callback_data='color:green'),
    InlineKeyboardButton(text="🐬", callback_data="color:blue"),
    InlineKeyboardButton(text="🌝", callback_data="color:yellow"),
    InlineKeyboardButton(text="💼", callback_data="color:brown"),
    InlineKeyboardButton(text="💥", callback_data="color:red"))

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Список задач", callback_data='list_all'),
        ],
        [
            InlineKeyboardButton(text="Синхронизировать списки", callback_data='sync'),
        ]
    ],
    resize_keyboard=True
)

back_button = InlineKeyboardButton(text="Назад", callback_data="back")
