import os
import urllib
from datetime import datetime
from django.core.files import File
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


# Create your models here.


class Student(models.Model):
    # id
    email = models.CharField(max_length=20, unique=True)
    # username
    username = models.CharField(blank=False, max_length=20, unique=True)
    # password
    password = models.CharField(max_length=6, blank=False)
    # Message
    song = models.ManyToManyField('Song', blank=True)

    def __str__(self):
        return self.email


class Song(models.Model):
    likedBy = models.CharField(Student, blank=True, null=True, max_length=30)
    title = models.CharField(max_length=30, default=None, blank=True, null=True)
    artist = models.TextField(blank=True, editable=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    year = models.IntegerField(blank=True, editable=True, null=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
