# Generated by Django 3.1.6 on 2021-02-15 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mscore', '0003_space_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='owner',
            field=models.ForeignKey(default='buzz0n', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
