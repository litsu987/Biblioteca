from django.db import models
from django.contrib.auth.models import User


class Centre(models.Model):
    nom = models.CharField(max_length=100)
    # Otros campos relevantes para el centro


class Cicle(models.Model):
    nom = models.CharField(max_length=100)
    # Otros campos relevantes para el ciclo


class TipusMaterial(models.Model):
    nom = models.CharField(max_length=50)


class Usuari(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_naixement = models.DateField()
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True)
    cicle = models.ForeignKey(Cicle, on_delete=models.SET_NULL, null=True)
    imatge = models.ImageField(upload_to='imatges/', null=True, blank=True)


class Catalog(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    imatge = models.ImageField(upload_to='imatges/', null=True, blank=True)


class ElementCatalog(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    tipus_material = models.ForeignKey(TipusMaterial, on_delete=models.CASCADE)
    # Otros campos relevantes


class Exemplar(models.Model):
    element_catalog = models.ForeignKey(ElementCatalog, on_delete=models.CASCADE)
    estat = models.CharField(max_length=50)
    # Otros campos relevantes


class Reserva(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    data_reserva = models.DateField(auto_now_add=True)


class Prestec(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    data_prestec = models.DateField(auto_now_add=True)
    data_retorn = models.DateField(null=True, blank=True)


class Peticio(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    titol_peticio = models.CharField(max_length=100)
    descripcio = models.TextField()
    data_peticio = models.DateField(auto_now_add=True)


class Log(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    accio = models.CharField(max_length=100)
    data_accio = models.DateTimeField(auto_now_add=True)


class ImatgeCatalog(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    imatge = models.ImageField(upload_to='imatges/')
