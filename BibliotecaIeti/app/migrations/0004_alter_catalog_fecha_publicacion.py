# Generated by Django 5.0.4 on 2024-05-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_catalog_fecha_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='fecha_publicacion',
            field=models.DateField(),
        ),
    ]
