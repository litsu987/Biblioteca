# Generated by Django 5.0.4 on 2024-04-24 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuari',
            old_name='nome',
            new_name='nom',
        ),
    ]
