# Generated by Django 5.1.7 on 2025-03-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_searcher', '0002_newssendrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssendrecord',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
