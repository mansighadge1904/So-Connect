# Generated by Django 5.1.6 on 2025-04-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_story_viewed_storyview'),
        ('users', '0003_remove_customuser_hobbies'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hobbies',
            field=models.ManyToManyField(blank=True, related_name='posts', to='users.hobby'),
        ),
    ]
