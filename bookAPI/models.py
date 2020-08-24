from django.db import models
from django.utils import timezone


# Create your models here.


class Book(models.Model):
    """Database model for book"""
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=150)
    published_on = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.name
