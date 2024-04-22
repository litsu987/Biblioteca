from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

TIPOS_MATERIAL_CHOICES = [
    ('llibre', 'Llibre'),
    ('CD', 'CD'),
    ('DVD', 'DVD'),
    ('BR', 'Blu-ray'),
    ('dispositiu', 'Dispositiu'),
]

class Centre(models.Model):
    nom = models.CharField(max_length=100)
   

class Cicle(models.Model):
    nom = models.CharField(max_length=100)
   

class TipusMaterial(models.Model):
    nom = models.CharField(max_length=50, choices=TIPOS_MATERIAL_CHOICES)

class Usuari(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default="") 
    nom = models.CharField(max_length=50, default="") 
    cognoms = models.CharField(max_length=100, default="") 
    data_naixement = models.DateField()
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True)
    cicle = models.ForeignKey(Cicle, on_delete=models.SET_NULL, null=True)
    imatge = models.ImageField(upload_to='imatges/', null=True, blank=True) 
    contrasenya_cifrada = models.CharField(max_length=128,default="")  # Longitud suficiente para almacenar la contraseña cifrada

    def set_password(self, raw_password):
        self.contrasenya_cifrada = make_password(raw_password)

class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    imatge = models.ImageField(upload_to='imatges/', null=True, blank=True)
    

class ElementCatalog(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    tipus_material = models.ForeignKey(TipusMaterial, on_delete=models.CASCADE)

    def __str__(self):
        return self.catalog.nom
    

class Llibre(Catalog):
    CDU = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13)
    editorial = models.CharField(max_length=100)
    collecio = models.CharField(max_length=100)
    autor = models.CharField(max_length=200, default="")
    pagines = models.IntegerField()

class CD(Catalog):
    discografica = models.CharField(max_length=100)
    estil = models.CharField(max_length=100)
    duracio = models.IntegerField()

class DVD(Catalog):
    productora = models.CharField(max_length=100)
    duracio = models.IntegerField()

class BR(Catalog):
    productora = models.CharField(max_length=100)
    duracio = models.IntegerField()


class Dispositiu(Catalog):
    modelo = models.CharField(max_length=100, default="")
    serie = models.CharField(max_length=100, default="")


class Exemplar(models.Model):
    element_catalog = models.ForeignKey(ElementCatalog, on_delete=models.CASCADE)
    estat = models.CharField(max_length=50)

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
    TIPO_LOG = (
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('FATAL', 'Fatal'),
    )
    
    usuari = models.CharField(max_length=100, null=True, blank=True)
    accio = models.CharField(max_length=100)
    data_accio = models.DateTimeField(auto_now_add=True)
    tipus = models.CharField(max_length=10, choices=TIPO_LOG, default="")

    def __str__(self):
        return f"{self.accio} - {self.tipus}"




class ImatgeCatalog(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    imatge = models.ImageField(upload_to='imatges/')