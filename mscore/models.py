from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.user.username


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=255)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Component(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='components')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time = models.TimeField(blank=True)
    totalTime = models.TimeField(blank=True)
    executors = models.ManyToManyField(User, related_name='executors')

    def __str__(self):
        return self.title
