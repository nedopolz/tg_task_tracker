from utils.API.baseAPI import BaseAPI, ToDoItem


class Controller:
    def __init__(self, connectors: list[BaseAPI], leader: BaseAPI):
        self.connectors_list = connectors
        self.leader = leader

    async def list_tasks(self) -> list[ToDoItem]:
        result = await self.leader.list_todo()
        return result

    async def add(self, todo: ToDoItem) -> bool:
        for connector in self.connectors_list:
            result = await connector.create_todo(todo)
        await self.leader.create_todo(todo)
        return True

    async def mark_as_done(self, task_text: str) -> bool:
        result = await self.leader.list_todo()
        task_text = task_text.replace("...", "")
        for task in result:
            if task_text in task.name:
                await self._mark_as_done(task)
        return True

    async def _mark_as_done(self, todo: ToDoItem) -> bool:
        for connector in self.connectors_list:
             await connector.mark_as_done(todo)
        await self.leader.mark_as_done(todo)
        return True

    async def sync_all(self) -> bool:
        result = await self.leader.list_todo()
        for connector in self.connectors_list:
            connector_tasks = await connector.list_todo()
            for todo in result:
                if todo not in connector_tasks:
                    await connector.create_todo(todo)
            for todo in connector_tasks:
                if todo not in result:
                    await connector.mark_as_done(todo)
        return True
