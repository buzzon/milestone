# Generated by Django 3.1.7 on 2021-05-22 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mscore', '0010_task_is_nested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='mscore.task'),
        ),
    ]
