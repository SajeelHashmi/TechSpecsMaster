from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .startDb import task,task2

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(task, 'interval', hours=12)
	scheduler.start()