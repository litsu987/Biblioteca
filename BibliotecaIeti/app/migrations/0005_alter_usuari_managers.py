# Generated by Django 5.0.4 on 2024-04-26 16:33

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_usuari_cognom_remove_usuari_nom'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuari',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
