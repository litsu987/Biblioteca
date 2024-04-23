import random
import os
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from .models import Centre, Cicle, TipusMaterial, Usuari, Catalog, ElementCatalog, Llibre, CD, BR,DVD, Dispositiu, Exemplar, Reserva, Prestec, Peticio, Log, ImatgeCatalog
from .models import TIPOS_MATERIAL_CHOICES
fake = Faker()

adjetivos = ["El secreto", "La última", "El misterioso", "El oscuro", "El perdido", "El legendario"]
sustantivos = ["reino", "tesoro", "poder", "destino", "legado", "encantamiento"]
tematicas = ["fantasía", "ciencia ficción", "misterio", "aventura", "romance", "terror"]

cd = [
    "Melodías en la Oscuridad",
    "Caminos del Silencio",
    "Sinfonía de la Aurora",
    "Ritmos del Cosmos",
    "Armonías del Viento",
    "Notas en el Abismo",
    "Sonidos de la Naturaleza",
    "Melancolía Nocturna",
    "Canciones del Horizonte",
    "Ecos del Pasado"
]

dvd = [
    "La Última Expedición",
    "Secretos en la Niebla",
    "El Misterio del Abismo",
    "Aventuras en el Tiempo",
    "Pesadilla en la Montaña",
    "Travesía por el Desierto",
    "El Laberinto de la Ciudad Perdida",
    "Intriga en el Castillo",
    "El Secreto del Bosque Encantado",
    "Misterios del Pasado"
]

disp = [
    "Eclipse 2000",
    "TechNova X",
    "CyberPro 3000",
    "StreamMaster S1",
    "SkyLink 500",
    "TechGear E2",
    "InnovaTech 360",
    "SmartEdge 4K",
    "DigitalPulse X",
    "NeoWave 800"
]

br = [
    "Espectros del Pasado",
    "Aventuras en Alta Definición",
    "Horizonte Azul",
    "Visiones del Futuro",
    "Ritmo de la Noche",
    "Misterios en HD",
    "Cinemasfera",
    "Alcance Óptico",
    "Energía Cinética",
    "Luz y Sombra"
]

def limpiar_bd():
    # Eliminar todos los registros de todas las tablas
    ImatgeCatalog.objects.all().delete()
    Log.objects.all().delete()
    Peticio.objects.all().delete()
    Prestec.objects.all().delete()
    Reserva.objects.all().delete()
    Exemplar.objects.all().delete()
    Dispositiu.objects.all().delete()
    BR.objects.all().delete()
    CD.objects.all().delete()
    Llibre.objects.all().delete()
    ElementCatalog.objects.all().delete()
    Catalog.objects.all().delete()
    Usuari.objects.all().delete()
    TipusMaterial.objects.all().delete()
    Cicle.objects.all().delete()
    Centre.objects.all().delete()
    User.objects.exclude(username='root').delete()





def seed_database(num_usuarios=10, num_centros=5, num_catalogos=20, num_elementos=50):
    limpiar_bd()