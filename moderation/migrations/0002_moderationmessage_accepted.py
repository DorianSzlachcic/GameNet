# Generated by Django 4.0.4 on 2022-06-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderationmessage',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
