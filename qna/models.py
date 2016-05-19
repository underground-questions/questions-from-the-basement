from django.db import models
from django.contrib.auth.models import User


class Answer(models.Model):
    text = models.TextField()
    votes = models.IntegerField(default=0)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    categories = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
