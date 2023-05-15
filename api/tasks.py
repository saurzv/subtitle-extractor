import re
import os
from celery import shared_task
from django.conf import settings
from .models import Subtitle

tempFolder=settings.MEDIA_ROOT

# extract content, start time, end time and make a json object
def parse_srt(path):
    with open(path, 'r', encoding='utf-8') as f:
        srt = f.read()
        sub_content = []
        for line in srt.split('\n\n'):
            if line != '' :
                idx = int(re.match(r'\d+', line).group())
                pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
                str = ' '.join(line[pos:].strip().split(' '))
                start_time=re.findall(r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
                end_time=re.findall(r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]

                sub_content.append({
                    'index':idx,
                    'content':str,
                    'start_time':start_time,
                    'end_time':end_time
                })

    return sub_content

@shared_task(bind=True)
def generateSRT(self, video_name, video_id):
    video_path = tempFolder+'uploads/'+video_name
    sub_name = tempFolder+'subs/'+video_name[:-4]

    os.system("ccextractor {} -o {}.srt".format(video_path, sub_name))

    sub_path = sub_name+'.srt'

    srt_list = parse_srt(sub_path)
    for srt in srt_list :
        Subtitle.objects.create(video_id=video_id, content=srt['content'], start_time=srt['start_time'], end_time=srt['end_time'])
    os.remove(video_path)