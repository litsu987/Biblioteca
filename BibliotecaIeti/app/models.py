from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

TIPOS_MATERIAL_CHOICES = [
    ('llibre', 'Llibre'),
    ('CD', 'CD'),
    ('DVD', 'DVD'),
    ('BR', 'Blu-ray'),
    ('dispositiu', 'Dispositiu'),
]

class Centre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Cicle(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class TipusMaterial(models.Model):
    nom = models.CharField(max_length=50, choices=TIPOS_MATERIAL_CHOICES)

    def __str__(self):
        return self.nom

class Usuari(AbstractUser):

    data_naixement = models.DateField(null=True, blank=True)
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True)
    cicle = models.ForeignKey(Cicle, on_delete=models.SET_NULL, null=True)
    imatge = models.ImageField(upload_to='imatges/', null=True, blank=True) 
    nom = models.CharField(max_length=30, blank=True)  
    cognom = models.CharField(max_length=30, blank=True)  
    groups = models.ManyToManyField('auth.Group', related_name="biblioteca_user_groups", blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name="biblioteca_user_permissions", blank=True)
    
    email = models.EmailField(("email"), unique=True, db_index=True)    
    telefon = models.CharField(max_length=15, blank=True)  # Agregar campo para el número de teléfono
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    ROLES_CHOICES = [
        ('Alumne', 'Alumne'),
        ('Admin', 'Admin'),
        ('Bibliotecari', 'Bibliotecari'),
    ]

    rol = models.CharField(max_length=50, choices=ROLES_CHOICES, default='', blank=True)
    autentificacio = models.BooleanField(default=False)  
    objects = UserManager()


class Catalog(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    imatge = models.ImageField(upload_to='static/', null=True, blank=True)

    def __str__(self):
        return self.nom


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
    cantidad = models.IntegerField(default=0)  # Agregar campo de cantidad
   
class CD(Catalog):
    discografica = models.CharField(max_length=100)
    estil = models.CharField(max_length=100)
    duracio = models.IntegerField()
    cantidad = models.IntegerField(default=0)  # Agregar campo de cantidad

class DVD(Catalog):
    productora = models.CharField(max_length=100)
    duracio = models.IntegerField()
    cantidad = models.IntegerField(default=0)  # Agregar campo de cantidad

class BR(Catalog):
    productora = models.CharField(max_length=100)
    duracio = models.IntegerField()
    cantidad = models.IntegerField(default=0)  # Agregar campo de cantidad

class Dispositiu(Catalog):
    modelo = models.CharField(max_length=100, default="")
    serie = models.CharField(max_length=100, default="")
    cantidad = models.IntegerField(default=0)  # Agregar campo de cantidad

class Exemplar(models.Model):
    element_catalog = models.ForeignKey(ElementCatalog, on_delete=models.CASCADE)
    estat = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.element_catalog} {self.estat}"  # Devuelve el nombre completo del usuario

class Reserva(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    data_reserva = models.DateField(auto_now_add=True)

class Prestec(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, default=1)

    data_prestec = models.DateField(auto_now_add=True)
    data_retorn = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Prestec de {self.catalog.nom} a {self.usuari} el {self.data_prestec}"



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
    imatge = models.ImageField(upload_to='static/')
