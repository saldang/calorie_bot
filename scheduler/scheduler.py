from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import send_daily_report

scheduler = BackgroundScheduler()

def start_scheduling(bot_app):
    scheduler.add_job(send_daily_report, 'cron', hour=23, minute=0, args=[bot_app])
    scheduler.start()