from django.db import models


class Lists(models.Model):
    url_list = models.TextField()
    story_list = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
