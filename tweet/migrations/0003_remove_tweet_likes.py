# Generated by Django 5.1.1 on 2024-09-04 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_tweet_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='likes',
        ),
    ]
