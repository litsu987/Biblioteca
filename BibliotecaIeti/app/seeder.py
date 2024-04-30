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

class CustomProvider(BaseProvider):
    def phone_number(self):
        return self.random_int(min=600000000, max=699999999)

fake.add_provider(CustomProvider)

def crear_usuarios(num_usuarios):
    roles_disponibles = ['Admin', 'Bibliotecari']
    # Contadores para los roles
    num_admin = Usuari.objects.filter(rol='Admin').count()
    num_bibliotecari = Usuari.objects.filter(rol='Bibliotecari').count()

    for _ in range(num_usuarios):
        # Seleccionar un rol aleatorio si aún hay disponibles
        if num_admin < 3:
            rol = 'Admin'
            num_admin += 1
        elif num_bibliotecari < 3:
            rol = 'Bibliotecari'
            num_bibliotecari += 1
        else:
            rol = ''  # No se asignará un rol si ya se alcanzó el límite

        username = fake.user_name()
        email = fake.email()
        password = "pa"
        data_naixement = fake.date_of_birth(minimum_age=18, maximum_age=90)
        imatge = fake.image_url()
        centre = Centre.objects.order_by('?').first()
        cicle = Cicle.objects.order_by('?').first()
        telefon = fake.phone_number()  # Añadir número de teléfono aleatorio
        nom = fake.first_name()  # Añadir nombre aleatorio
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
            nom=nom,
            cognom=cognom, # Añadir nombre aleatorio
            rol=rol  # Asignar el rol seleccionado
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
        Cicle.objects.create(nom=ciclo)


def crear_tipos_material():
    for tipo in TIPOS_MATERIAL_CHOICES:
        tipo_existente = TipusMaterial.objects.filter(nom=tipo[0]).exists()
        if not tipo_existente:
            TipusMaterial.objects.create(nom=tipo[0])


def crear_catalogo(num_catalogos):
    for _ in range(num_catalogos):
        catalog = Catalog.objects.create(
            nom=fake.word(),  # Cambiamos de fake.catch_phrase() a fake.word()
            descripcio=fake.paragraph()
        )
        ImatgeCatalog.objects.create(
            catalog=catalog,
            imatge=fake.image_url()
        )
        tipo_material = random.choice(TIPOS_MATERIAL_CHOICES)
        tipo_material_obj = TipusMaterial.objects.get(nom=tipo_material[0])
        ElementCatalog.objects.create(
            catalog=catalog,
            tipus_material=tipo_material_obj
        )
        if tipo_material[0] == 'llibre':
            nombre_libro = fake.catch_phrase()
            isbn13 = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            Llibre.objects.create(
                nom=nombre_libro,  # Cambiamos de fake.catch_phrase() a fake.word()
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
                nom=nombre_cd,  # Cambiamos de fake.catch_phrase() a fake.word()
                discografica=fake.company(),
                estil=fake.word(),
                duracio=random.randint(30, 120)
            )
        elif tipo_material[0] == 'DVD':
            nombre_dvd = f"{random.choice(dvd)}"
            DVD.objects.create(
                nom=nombre_dvd,  # Cambiamos de fake.catch_phrase() a fake.word()
                productora=fake.company(),
                duracio=random.randint(60, 180)
            )
        elif tipo_material[0] == 'BR':
            nombre_br = f"{random.choice(br)}"
            BR.objects.create(
                nom=nombre_br,  # Cambiamos de fake.catch_phrase() a fake.word()
                productora=fake.company(),
                duracio=random.randint(60, 180)
            )
        elif tipo_material[0] == 'dispositiu':
            nombre_disp = f"{random.choice(disp)}"
            Dispositiu.objects.create(
                nom= nombre_disp ,  # Cambiamos de fake.catch_phrase() a fake.word()
                modelo=fake.word(),
                serie=fake.uuid4(),
            )





def crear_reservas_prestamos_peticiones(num_elementos):
    usuarios = Usuari.objects.all()
    elementos = ElementCatalog.objects.all()
    for _ in range(num_elementos):
        usuario = random.choice(usuarios)
        elemento = random.choice(elementos)
        exemplar = Exemplar.objects.create(
            element_catalog=elemento,
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
                exemplar=exemplar,
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
    crear_tipos_material()
    crear_centros(num_centros)
    crear_ciclos()
    crear_usuarios(num_usuarios)
    crear_catalogo(num_catalogos)
    crear_autores_y_libros()
    crear_reservas_prestamos_peticiones(num_elementos)