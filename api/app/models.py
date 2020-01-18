from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Frame(models.Model):
    video = models.ForeignKey("Video", models.CASCADE)
    frame_number = models.IntegerField(blank=False, default=0)
    date_time = models.DateTimeField(blank=True, null=True, default=None)  # Used for actual CCTV footage.
    count = models.IntegerField(blank=False)
    timestamp = models.FloatField(blank=False, default=0)  # If using video, timestamp is the timestamp of the video from start
    anomaly = models.BooleanField(blank=False, default=False)

class Video(models.Model):
    url = models.URLField(blank=True)
    fileName = models.CharField(max_length=255, blank=True)
    isUrl = models.BooleanField(default=True)

