from django.db import models


# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
