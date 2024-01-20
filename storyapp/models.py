from django.db import models


# Create your models here.

class GeneratedStory(models.Model):
    generated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
