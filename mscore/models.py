from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.user.username


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    title = models.CharField(blank=True, max_length=255)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('space-detail', args=[str(self.pk)])


class RenewSpaceModelForm(ModelForm):
    class Meta:
        model = Space
        fields = ['title']


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
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return self.title

    # ОБЯЗАТЕЛЬНО УБРАТЬ ЭТОТ БРЕД ПОСЛЕ ПОДКЛЮЧЕНИЯ AJAX
    @staticmethod
    def get_absolute_url():
        from django.urls import reverse
        return reverse('space-list')


class Component(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='components')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time = models.TimeField(blank=True)
    totalTime = models.TimeField(blank=True)
    executors = models.ManyToManyField(User, related_name='executors')

    def __str__(self):
        return self.title
