import re
import os
import boto3
import json
from celery import shared_task
from django.conf import settings
from server.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

tempFolder = os.path.join(settings.BASE_DIR, 'media/')


def parse_srt(path):
    with open(path, 'r', encoding='utf-8') as f:
        srt = f.read()
        sub_content = []
        for line in srt.split('\n\n'):
            if line != '':
                idx = int(re.match(r'\d+', line).group())
                pos = re.search(
                    r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
                str = ' '.join(line[pos:].strip().split(' '))
                start_time = re.findall(
                    r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
                end_time = re.findall(
                    r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]

                sub_content.append({
                    'index': idx,
                    'content': str,
                    'start_time': start_time,
                    'end_time': end_time
                })

    return sub_content


def get_path(video_name):
    return [os.path.join(tempFolder, 'uploads', video_name), os.path.join(tempFolder, 'subs', video_name[:-4]+'.srt')]


@shared_task(bind=True)
def generateSRT(self, video_name, video_id):
    video_path, subtitle_path = get_path(video_name)
    os.system("ccextractor {} -o {}".format(video_path, subtitle_path))
    srt_list = parse_srt(subtitle_path)

    dynamo_client = boto3.resource(service_name='dynamodb', region_name='ap-south-1',
                                   aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    table = dynamo_client.Table('subs')
    data = {'test-key-1': str(video_id), 'srt': json.dumps(srt_list)}
    table.put_item(Item=data)

    os.remove(video_path)
    os.remove(subtitle_path)
