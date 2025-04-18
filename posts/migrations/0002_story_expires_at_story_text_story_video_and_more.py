# Generated by Django 5.1.6 on 2025-04-04 15:15

import posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='expires_at',
            field=models.DateTimeField(default=posts.models.get_expiry_time),
        ),
        migrations.AddField(
            model_name='story',
            name='text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='stories/'),
        ),
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='stories/'),
        ),
    ]
