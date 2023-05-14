from celery import shared_task
import os

@shared_task(bind=True)
def generateSRT(self, video_path):
    os.system("ccextractor {} -o test.srt".format(video_path))