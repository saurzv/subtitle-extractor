from django.db import models


class Video(models.Model):
    file = models.FileField(upload_to='uploads/')


# not used in production
class Subtitle(models.Model):
    content = models.CharField(max_length=1000, default='')
    start_time = models.CharField(max_length=255, default='')
    end_time = models.CharField(max_length=255, default='')
