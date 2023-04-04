from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class APIException(Exception):
    pass


class ColorEnum(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    BROWN = "brown"


@dataclass
class ToDoItem:
    name: str
    is_done: bool
    color: ColorEnum | None


class BaseAPI(ABC):
    @abstractmethod
    async def create_todo(self, todo: ToDoItem) -> bool | APIException:
        pass

    @abstractmethod
    async def mark_as_done(self, todo: ToDoItem) -> bool | APIException:
        pass

    @abstractmethod
    async def list_todo(self) -> list[ToDoItem | None] | APIException:
        pass

    @abstractmethod
    async def remove_todo(self, todo: ToDoItem) -> bool | APIException:
        pass

    @staticmethod
    def color_to_enum(color: str) -> ColorEnum:
        match color:
            case "🐬голубая":
                return ColorEnum.BLUE
            case "🍀Зелёная":
                return ColorEnum.GREEN
            case "🌝Желтая":
                return ColorEnum.YELLOW
            case "💥Красная":
                return ColorEnum.RED
            case "💼Коричневая":
                return ColorEnum.BROWN

    @staticmethod
    def enum_to_color(enum: ColorEnum) -> str:
        match enum:
            case enum.RED:
                return "💥Красная"
            case enum.BLUE:
                return "🐬голубая"
            case enum.BROWN:
                return "💼Коричневая"
            case enum.GREEN:
                return "🍀Зелёная"
            case enum.YELLOW:
                return "🌝Желтая"
