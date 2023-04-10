from utils.set_bot_commands import set_default_commands


async def sync_job():
    from loader import controller

    await controller.sync_all()


def schedule_jobs():
    scheduler.add_job(sync_job, "interval", minutes=5)


async def on_startup(dp):
    import middlewares

    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)
    await set_default_commands(dp)
    schedule_jobs()


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp
    from loader import scheduler, controller

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
