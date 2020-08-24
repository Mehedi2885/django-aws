from django.db import models
from django.db.models import Q

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    rollNo = models.IntegerField(unique=True)
    marks = models.IntegerField()
    subjects = models.CharField(max_length=150)

    def __str__(self):
        return self.name

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     rollNo = models.IntegerField(unique=True)
#     marks = models.IntegerField()
#     subjects = models.CharField(max_length=150)
#
#     def __str__(self):
#         return self.name
