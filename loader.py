from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from data.config import NOTION_API_KEY, NOTION_DATABASE_ID, NOTION_PAGE_ID, TODOIST_API_KEY, TODOIST_PROJECT_ID
from utils.API.APIcontroller import Controller
from utils.API.notionAPI import Notion
from utils.API.todoistAPI import ToDoist

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
notion = Notion(api_key=NOTION_API_KEY, database_id=NOTION_DATABASE_ID, page_id=NOTION_PAGE_ID)
todoist = ToDoist(api_key=TODOIST_API_KEY, project_id=TODOIST_PROJECT_ID)
controller = Controller(leader=notion, connectors=[todoist])
scheduler = AsyncIOScheduler()

__all__ = ["bot", "storage", "dp", "notion", "todoist", "controller", "scheduler"]
