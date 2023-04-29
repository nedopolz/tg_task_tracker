import os

from dotenv import load_dotenv

load_dotenv()

admins = ["419519710", "438757516"]
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

NOTION_API_KEY = str(os.getenv("NOTION_API_KEY"))
NOTION_DATABASE_ID = str(os.getenv("NOTION_DATABASE_ID"))
NOTION_PAGE_ID = str(os.getenv("NOTION_PAGE_ID"))

TODOIST_API_KEY = str(os.getenv("TODOIST_API_KEY"))
TODOIST_PROJECT_ID = str(os.getenv("TODOIST_PROJECT_ID"))
