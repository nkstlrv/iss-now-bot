from apscheduler.schedulers.asyncio import AsyncIOScheduler


def schedule_jobs(job, dispatcher):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=30, args=(dispatcher,))
    scheduler.start()