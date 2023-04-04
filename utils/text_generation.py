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


def create_active_to_do_message(todos: list[ToDoItem]) -> str:
    base_text = "{} - {} - {}\n"
    result = "На сегодня у нас:\n"
    for count, todo in enumerate(todos):
        result += base_text.format(count+1, todo.name, enum_to_color(todo.color))
    return result
