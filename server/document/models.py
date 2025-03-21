from django.db import models

class Document(models.Model):
    document = models.URLField(max_length=1000)
    summary = models.TextField(max_length=10000, default = "")
    analysis = models.JSONField(default = [])
