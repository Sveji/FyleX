from django.db import models
from user.models import CustomUser

# MODEL FOR EVERY DOCUMENT
class Document(models.Model):
    document = models.URLField(max_length=1000)
    summary = models.TextField(max_length=10000, default = "")
    analysis = models.JSONField(default = [])
    review = models.TextField(max_length=10000, default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=256, default="")

