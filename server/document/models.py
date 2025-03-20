from django.db import models

class Document(models.Model):
    document = models.URLField(max_length=1000)