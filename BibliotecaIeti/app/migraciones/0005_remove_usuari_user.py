# Generated by Django 5.0.4 on 2024-04-23 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_log_tipus_alter_log_usuari'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuari',
            name='user',
        ),
    ]