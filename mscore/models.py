from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.user.username


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='owned_spaces')
    title = models.CharField(blank=True, max_length=255)
    publish_date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='spaces', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('space_detail', args=[str(self.pk)])


def tomorrow():
    return datetime.now() + timedelta(days=1)


class Task(models.Model):
    STATUS = [
        ('A', 'Approval'),
        ('W', 'Waiting'),
        ('P', 'Progressing'),
        ('R', 'Ready'),
        ('C', 'Correction')
    ]

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='A')
    publish_date = models.DateTimeField(auto_now_add=True, editable=False)
    initial_date = models.DateTimeField(default=datetime.now, blank=True)
    deadline = models.DateTimeField(default=tomorrow, blank=True)

    class Meta:
        ordering = ['-deadline', 'status']

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
