# Generated by Django 3.1.7 on 2021-04-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_dissertation_docfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfields',
            name='has_disserta',
            field=models.BooleanField(default=False),
        ),
    ]
