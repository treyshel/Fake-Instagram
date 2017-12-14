from django.shortcuts import render

from django.db import models


class Document(models.Model):
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='documents/')
    time_uploaded = models.DateTimeField(auto_now_add=True)