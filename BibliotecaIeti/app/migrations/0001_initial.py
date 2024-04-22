# Generated by Django 5.0.4 on 2024-04-22 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
                ('imatge', models.ImageField(blank=True, null=True, upload_to='imatges/')),
            ],
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipusMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('llibre', 'Llibre'), ('CD', 'CD'), ('DVD', 'DVD'), ('BR', 'Blu-ray'), ('dispositiu', 'Dispositiu')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BR',
            fields=[
                ('catalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.catalog')),
                ('productora', models.CharField(max_length=100)),
                ('duracio', models.IntegerField()),
            ],
            bases=('app.catalog',),
        ),
        migrations.CreateModel(
            name='CD',
            fields=[
                ('catalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.catalog')),
                ('discografica', models.CharField(max_length=100)),
                ('estil', models.CharField(max_length=100)),
                ('duracio', models.IntegerField()),
            ],
            bases=('app.catalog',),
        ),
        migrations.CreateModel(
            name='Dispositiu',
            fields=[
                ('catalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.catalog')),
                ('modelo', models.CharField(default='', max_length=100)),
                ('serie', models.CharField(default='', max_length=100)),
            ],
            bases=('app.catalog',),
        ),
        migrations.CreateModel(
            name='DVD',
            fields=[
                ('catalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.catalog')),
                ('productora', models.CharField(max_length=100)),
                ('duracio', models.IntegerField()),
            ],
            bases=('app.catalog',),
        ),
        migrations.CreateModel(
            name='Llibre',
            fields=[
                ('catalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.catalog')),
                ('CDU', models.CharField(max_length=100)),
                ('ISBN', models.CharField(max_length=13)),
                ('editorial', models.CharField(max_length=100)),
                ('collecio', models.CharField(max_length=100)),
                ('autor', models.CharField(default='', max_length=200)),
                ('pagines', models.IntegerField()),
            ],
            bases=('app.catalog',),
        ),
        migrations.CreateModel(
            name='ElementCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.catalog')),
                ('tipus_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipusmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='Exemplar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estat', models.CharField(max_length=50)),
                ('element_catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.elementcatalog')),
            ],
        ),
        migrations.CreateModel(
            name='ImatgeCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imatge', models.ImageField(upload_to='imatges/')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.catalog')),
            ],
        ),
        migrations.CreateModel(
            name='Usuari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=254)),
                ('nom', models.CharField(default='', max_length=50)),
                ('cognoms', models.CharField(default='', max_length=100)),
                ('data_naixement', models.DateField()),
                ('imatge', models.ImageField(blank=True, null=True, upload_to='imatges/')),
                ('contrasenya_cifrada', models.CharField(default='', max_length=128)),
                ('centre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.centre')),
                ('cicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.cicle')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_reserva', models.DateField(auto_now_add=True)),
                ('exemplar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.exemplar')),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuari')),
            ],
        ),
        migrations.CreateModel(
            name='Prestec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prestec', models.DateField(auto_now_add=True)),
                ('data_retorn', models.DateField(blank=True, null=True)),
                ('exemplar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.exemplar')),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuari')),
            ],
        ),
        migrations.CreateModel(
            name='Peticio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titol_peticio', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
                ('data_peticio', models.DateField(auto_now_add=True)),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuari')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accio', models.CharField(max_length=100)),
                ('data_accio', models.DateTimeField(auto_now_add=True)),
                ('usuari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuari')),
            ],
        ),
    ]
