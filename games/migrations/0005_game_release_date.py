# Generated by Django 4.0.4 on 2022-05-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_game_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='release_date',
            field=models.DateField(blank=True, help_text='Data wydania gry', null=True),
        ),
    ]
