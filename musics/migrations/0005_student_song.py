# Generated by Django 3.1.7 on 2021-04-27 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0004_auto_20210425_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='song',
            field=models.ManyToManyField(blank=True, to='musics.Song'),
        ),
    ]
