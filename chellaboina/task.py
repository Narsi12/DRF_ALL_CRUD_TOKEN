from celery import shared_task
import time

@shared_task
def handle_sleep():
    time.sleep(10)
    return {'Message':"Task is completed"}