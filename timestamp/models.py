from django.db import models


# Create your models here.

# Creating  a Video Database

class Video(models.Model):
    video_id = models.CharField(unique=True, max_length=255)
    chapter_titles = models.JSONField()





