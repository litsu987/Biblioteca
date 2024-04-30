import random
import os
from .models import *
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from .models import Centre, Cicle, TipusMaterial, Usuari, Catalog, ElementCatalog, Llibre, CD, BR, DVD, Dispositiu, Exemplar, Reserva, Prestec, Peticio, Log, ImatgeCatalog
from .models import TIPOS_MATERIAL_CHOICES
from faker.providers import BaseProvider
fake = Faker('es_ES')
from django.db import connection


adjetivos = ["El secreto", "La última", "El misterioso", "El oscuro", "El perdido", "El legendario", "El antiguo", "El majestuoso", "El intrépido", "El eterno", "El enigmático", "El dorado", "El fantástico", "El brillante", "El mágico", "El épico", "El inolvidable", "El infinito", "El inmortal", "El resplandeciente", "El prodigioso", "El celestial", "El etéreo", "El sagrado", "El inquietante", "El titánico", "El magnífico", "El cósmico", "El sublime", "El asombroso", "El deslumbrante", "El enérgico", "El intrépido", "El poderoso", "El enigmático", "El sorprendente", "El deslumbrante", "El imponente", "El arcano", "El maravilloso", "El incandescente", "El hipnótico", "El majestuoso", "El vibrante", "El impredecible", "El enigmático", "El exuberante", "El radiante"]
sustantivos = ["reino", "tesoro", "poder", "destino", "legado", "encantamiento", "criatura", "reliquia", "secreto", "profecía", "maravilla", "abismo", "corazón", "leyenda", "destello", "rumor", "susurro", "ocaso", "sendero", "arcano", "amanecer", "eco", "abrazo", "velo", "destino", "laberinto", "fragmento", "sueño", "vigilia", "destino", "tesoro", "poder", "destino", "legado", "encantamiento", "criatura", "reliquia", "secreto", "profecía", "maravilla", "abismo", "corazón", "leyenda", "destello", "rumor", "susurro", "ocaso"]
tematicas = ["fantasía", "ciencia ficción", "misterio", "aventura", "romance", "terror", "histórico", "distopía", "thriller", "comedia", "surrealismo", "post-apocalíptico", "steampunk", "mitología", "ciberpunk", "filosófico", "viaje en el tiempo", "magia oscura", "ciencia fantástica", "intriga política", "cyberthriller", "realismo mágico", "folclore urbano", "epopeya", "cuento de hadas", "guerra galáctica", "rebelión cósmica", "invasión extraterrestre", "odisea espacial", "legado ancestral", "magia", "sueño", "rebelión", "destino", "futuro", "esperanza", "oscuridad", "poder", "misterio", "encuentro", "renacimiento", "venganza", "pasión", "resistencia", "alma", "cambio", "sacrificio", "odio", "renovación"]

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
   
    TipusMaterial.objects.all().delete()
    Llibre.objects.all().delete()
   # Usuari.objects.all().delete()
    Centre.objects.all().delete()
    Cicle.objects.all().delete()
    Catalog.objects.all().delete()
    ElementCatalog.objects.all().delete()
    CD.objects.all().delete()
    BR.objects.all().delete()
    DVD.objects.all().delete()
    Dispositiu.objects.all().delete()
    Exemplar.objects.all().delete()
    Reserva.objects.all().delete()
    Prestec.objects.all().delete()
    Peticio.objects.all().delete()

   
  

class CustomProvider(BaseProvider):
    def phone_number(self):
        return self.random_int(min=600000000, max=699999999)

fake.add_provider(CustomProvider)

def crear_usuarios(num_usuarios):
    roles_disponibles = ['Admin', 'Bibliotecari', 'Alumne']
    # Contadores para los roles
    num_admin = Usuari.objects.filter(rol='Admin').count()
    num_bibliotecari = Usuari.objects.filter(rol='Bibliotecari').count()
    num_alumne = Usuari.objects.filter(rol='Alumne').count()

    for _ in range(num_usuarios):
        # Seleccionar un rol aleatorio si aún hay disponibles
        if num_bibliotecari < 3:
            rol = 'Bibliotecari'
            num_bibliotecari += 1
            autentificacio = True  # Establecer autenticación en True para el rol de "Bibliotecari"
        elif num_admin < 3:
            rol = 'Admin'
            num_admin += 1
            autentificacio = True  # Establecer autenticación en True para el rol de "Admin"
        else:
            # Si ya hay suficientes bibliotecarios y administradores,
            # crear usuarios con el rol de "Alumne" exclusivamente
            rol = 'Alumne'
            autentificacio = False  # Para otros roles, la autenticación se establece en False por defecto

        username = fake.user_name()
        email = fake.email()
        password = "pa"
        data_naixement = fake.date_of_birth(minimum_age=18, maximum_age=90)
        imatge = fake.image_url()
        centre = Centre.objects.order_by('?').first()
        cicle = Cicle.objects.order_by('?').first()
        telefon = fake.phone_number()  # Añadir número de teléfono aleatorio
        first_name = fake.first_name() 
        last_name = fake.last_name() 
        cognom = fake.last_name()

        # Crear usuario
        usuari = Usuari.objects.create(
            username=username,
            email=email,
            data_naixement=data_naixement,
            imatge=imatge,
            centre=centre,
            cicle=cicle,
            telefon=telefon,  # Añadir número de teléfono
            first_name=first_name,
            last_name=last_name,
            cognom=cognom, # Añadir nombre aleatorio
            rol=rol,  # Asignar el rol seleccionado
            autentificacio=autentificacio  # Establecer autenticación
        )

        # Configurar contraseña
        usuari.set_password(password)
        usuari.save()




def crear_centros(num_centros):
    for _ in range(num_centros):
        Centre.objects.create(nom=fake.company())

def crear_ciclos():
    ciclos = ["AWS", "AMS", "ASIX"]
    for ciclo in ciclos:
        if not Cicle.objects.filter(nom=ciclo).exists():
            Cicle.objects.create(nom=ciclo)



def crear_tipos_material():
    for tipo in TIPOS_MATERIAL_CHOICES:
        tipo_existente = TipusMaterial.objects.filter(nom=tipo[0]).exists()
        if not tipo_existente:
            TipusMaterial.objects.create(nom=tipo[0])


def crear_catalogo(num_catalogos):
    for _ in range(num_catalogos):
        catalog = Catalog.objects.create(
            nom=fake.word(),
            descripcio=fake.paragraph()
        )
        ImatgeCatalog.objects.create(
            catalog=catalog,
            imatge=fake.image_url()
        )
        tipo_material = random.choice(TIPOS_MATERIAL_CHOICES)
        tipo_material_obj = TipusMaterial.objects.get(nom=tipo_material[0])
        element_catalog = ElementCatalog.objects.create(
            catalog=catalog,
            tipus_material=tipo_material_obj
        )
        if tipo_material[0] == 'llibre':
            nombre_libro = fake.catch_phrase()
            isbn13 = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            Llibre.objects.create(
                nom=nombre_libro,
                CDU=fake.isbn13(),
                ISBN=isbn13,
                editorial=fake.company(),
                collecio=fake.catch_phrase(),
                autor=fake.name(),
                pagines=random.randint(100, 1000)
            )
        elif tipo_material[0] == 'CD':
            nombre_cd = f"{random.choice(cd)}"
            CD.objects.create(
                nom=nombre_cd,
                discografica=fake.company(),
                estil=fake.word(),
                duracio=random.randint(30, 120)
            )
        elif tipo_material[0] == 'DVD':
            nombre_dvd = f"{random.choice(dvd)}"
            DVD.objects.create(
                nom=nombre_dvd,
                productora=fake.company(),
                duracio=random.randint(60, 180)
            )
        elif tipo_material[0] == 'BR':
            nombre_br = f"{random.choice(br)}"
            BR.objects.create(
                nom=nombre_br,
                productora=fake.company(),
                duracio=random.randint(60, 180)
            )
        elif tipo_material[0] == 'dispositiu':
            nombre_disp = f"{random.choice(disp)}"
            Dispositiu.objects.create(
                nom= nombre_disp,
                modelo=fake.word(),
                serie=fake.uuid4(),
            )



def crear_reservas_prestamos_peticiones(num_elementos):
    usuarios = Usuari.objects.all()
    element_catalogs = ElementCatalog.objects.all()  # Obtener todos los ElementCatalog
    for _ in range(num_elementos):
        usuario = random.choice(usuarios)
        element_catalog = random.choice(element_catalogs)
        exemplar = Exemplar.objects.create(
            element_catalog=element_catalog,  # Asignar directamente el ElementCatalog
            estat=random.choice(['Disponible', 'Prestado', 'Reservado'])
        )
        if exemplar.estat == 'Reservado':
            Reserva.objects.create(
                usuari=usuario,
                exemplar=exemplar,
                data_reserva=fake.date_time_this_year()
            )
        elif exemplar.estat == 'Prestado':
            Prestec.objects.create(
                usuari=usuario,
                catalog=element_catalog.catalog,  # Usar el catalog asociado al ElementCatalog
                data_prestec=fake.date_time_this_year(),
                data_retorn=fake.date_time_this_year() + timezone.timedelta(days=random.randint(7, 30))
            )
    for _ in range(num_elementos):
        Peticio.objects.create(
            usuari=random.choice(usuarios),
            titol_peticio=fake.catch_phrase(),
            descripcio=fake.paragraph(),
            data_peticio=fake.date_time_this_year()
        )

def crear_autores_y_libros(num_autores=100):
    for _ in range(num_autores):
        autor_nombre = fake.name()
        num_libros = random.randint(1, 10)  # Número aleatorio de libros por autor
        for _ in range(num_libros):
            nombre_libro = f"{random.choice(adjetivos)} {random.choice(sustantivos)} del {random.choice(tematicas)}"
            isbn13 = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            Llibre.objects.create(
                nom=nombre_libro,
                CDU=fake.isbn13(),
                ISBN=isbn13,
                editorial=fake.company(),
                collecio=fake.catch_phrase(),
                autor=autor_nombre,
                pagines=random.randint(100, 1000)
            )


def seed_database(num_usuarios=10, num_centros=5, num_catalogos=20, num_elementos=50):
    limpiar_bd()
    