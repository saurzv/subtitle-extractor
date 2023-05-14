from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    file=models.FileField(upload_to='uploads/')

class Subtitle(models.Model):
    video = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    subtitle = models.JSONField()