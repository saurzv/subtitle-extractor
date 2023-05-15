from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    file=models.FileField(upload_to='uploads/')

class Subtitle(models.Model):
    video_id = models.CharField(max_length=255)
    content = models.CharField(max_length=1000, default='')
    start_time = models.CharField(max_length=255, default='')
    end_time = models.CharField(max_length=255, default='')