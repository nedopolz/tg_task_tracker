from notion_client import AsyncClient

from utils.API.baseAPI import BaseAPI, ToDoItem, APIException, ColorEnum


class Notion(BaseAPI):
    def __init__(self, api_key, page_id, database_id):
        self.database_id = database_id
        self.page_id = page_id
        self.notion = AsyncClient(auth=api_key)

    async def list_todo(self) -> list[ToDoItem | None] | APIException:
        filter = {
            "and": [
                {
                    "property": "Сделано?",
                    "checkbox": {
                        "equals": False,
                    },
                },
                {
                    "property": "Когда начать?",
                    "select": {
                        "equals": "Сегодня",
                    },
                },
            ]
        }
        items = await self.notion.databases.query(
            database_id=self.database_id, filter=filter, page_size=20
        )
        results = []
        for item in items.get("results"):
            todo = ToDoItem(
                name=item["properties"]["Обезьянопонятная задача"]["title"][0][
                    "plain_text"
                ],
                is_done=item["properties"]["Сделано?"]["checkbox"],
                color=self.color_to_enum(
                    item["properties"]["Цвет задачи"]["select"]["name"]
                ),
            )
            results.append(todo)
        return results

    async def create_todo(self, todo: ToDoItem) -> bool | APIException:
        parent = {"type": "database_id", "database_id": self.database_id}
        data = {
            "properties": {
                "Сделано?": {"checkbox": False, "type": "checkbox"},
                "Когда начать?": {"select": {"name": "Сегодня"}},
                "Обезьянопонятная задача": {
                    "id": "title",
                    "title": [
                        {
                            "annotations": {
                                "bold": False,
                                "code": False,
                                "color": "default",
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                            },
                            "href": None,
                            "plain_text": todo.name,
                            "text": {"content": todo.name, "link": None},
                            "type": "text",
                        }
                    ],
                    "type": "title",
                },
                "Цвет задачи": {
                    "id": "SkuO",
                    "select": {"name": self.enum_to_color(todo.color)},
                    "type": "select",
                },
            }
        }

        await self.notion.pages.create(parent=parent, **data)
        return True

    async def get_todo_id(self, name: str) -> str | None:
        filter = {
            "and": [
                {
                    "property": "Сделано?",
                    "checkbox": {
                        "equals": False,
                    },
                },
                {
                    "property": "Когда начать?",
                    "select": {
                        "equals": "Сегодня",
                    },
                },
                {"property": "Обезьянопонятная задача", "title": {"equals": name}},
            ]
        }
        items = await self.notion.databases.query(
            database_id=self.database_id, filter=filter, page_size=20
        )
        for item in items.get("results"):
            return item["id"]
        return None

    async def mark_as_done(self, todo: ToDoItem) -> bool | APIException:
        page_id = await self.get_todo_id(todo.name)
        if not page_id:
            return False
        data = {"properties": {"Сделано?": {"checkbox": True, "type": "checkbox"}}}
        await self.notion.pages.update(page_id=page_id, **data)
        return True

    async def remove_todo(self, todo: ToDoItem) -> bool | APIException:
        return False
