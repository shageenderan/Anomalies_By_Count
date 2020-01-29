from django.db import models

# This file contains the classes that define our data models to be created in the databse.

class Frame(models.Model):
    video = models.ForeignKey("Video", models.CASCADE) # Foreign key that points to the video the frame belongs to.
    frame_number = models.IntegerField(blank=False, default=0) # Frame number with respect to the video. Used for sorts
    date_time = models.DateTimeField(blank=True, null=True, default=None)  # Used for actual CCTV footage datetime
    count = models.IntegerField(blank=False) # Number of people counted in the frame
    timestamp = models.FloatField(blank=False, default=0)  # If using video, timestamp is the timestamp of the video from start
    anomaly = models.BooleanField(blank=False, default=False) # Boolean value for whether an anomaly exist in the frame

class Video(models.Model):
    url = models.URLField(blank=True) # URL of the video given
    fileName = models.CharField(max_length=255, blank=True) # Filename of the video given
    isUrl = models.BooleanField(default=True) # Boolean check to see if video is to be downloaded from the URL.

