from todoist_api_python.api_async import TodoistAPIAsync

from utils.API.baseAPI import BaseAPI, APIException, ToDoItem


class ToDoist(BaseAPI):
    def __init__(self, api_key, project_id):
        self.todoist = TodoistAPIAsync(api_key)
        self.project_id = project_id

    async def create_todo(self, todo: ToDoItem) -> bool | APIException:
        await self.todoist.add_task(
            content=todo.name,
            labels=[self.enum_to_color(todo.color)],
            project_id=self.project_id,
        )
        return True

    async def get_id_by_name(self, name: str) -> str:
        name = name.replace(",", "")
        name = name[:15]
        item = await self.todoist.get_tasks(**{"filter": f"search: {name}"})
        if len(item) > 0:
            return item[0].id
        return ""

    async def mark_as_done(self, todo: ToDoItem) -> bool | APIException:
        task_id = await self.get_id_by_name(todo.name)
        if not task_id:
            return False
        await self.todoist.close_task(task_id=task_id)
        return True

    async def list_todo(self) -> list[ToDoItem | None] | APIException:
        items = await self.todoist.get_tasks(project_id=self.project_id)
        results = []
        for item in items:
            color = item.labels[0] if len(item.labels) > 0 else None
            todo = ToDoItem(
                color=self.color_to_enum(color), name=item.content, is_done=False
            )
            results.append(todo)
        return results

    async def remove_todo(self, todo: ToDoItem) -> bool | APIException:
        return False
