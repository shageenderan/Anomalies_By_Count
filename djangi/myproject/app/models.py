from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Frame(models.Model):
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(null=False)
    count = models.IntegerField(null=False)

    def __str__(self):
        return self.title
