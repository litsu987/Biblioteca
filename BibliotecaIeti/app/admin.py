from django.contrib import admin
from .models import Centre, Cicle, TipusMaterial, Usuari, ElementCatalog, Exemplar, Reserva, Prestec, Peticio, Log, ImatgeCatalog, Llibre, CD, BR,DVD, Dispositiu

@admin.register(Centre)
class CentreAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Cicle)
class CicleAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(TipusMaterial)
class TipusMaterialAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Usuari)
class UsuariAdmin(admin.ModelAdmin):
    list_display = ('user','email','contrasenya_cifrada','cognoms', 'data_naixement', 'centre', 'cicle', 'imatge')


@admin.register(ElementCatalog)
class ElementCatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'tipus_material')

@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('element_catalog', 'estat')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'exemplar', 'data_reserva')

@admin.register(Prestec)
class PrestecAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'exemplar', 'data_prestec', 'data_retorn')

@admin.register(Peticio)
class PeticioAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'titol_peticio', 'descripcio', 'data_peticio')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'accio', 'data_accio', 'tipus')

@admin.register(ImatgeCatalog)
class ImatgeCatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'imatge')

@admin.register(Llibre)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('nom', 'CDU', 'ISBN', 'editorial', 'collecio', 'pagines')

@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ('nom', 'discografica', 'estil', 'duracio')

@admin.register(DVD)
class DVDAdmin(admin.ModelAdmin):
    list_display = ('nom', 'productora', 'duracio')

@admin.register(BR)
class BRAdmin(admin.ModelAdmin):
    list_display = ('nom', 'productora','duracio')

@admin.register(Dispositiu)
class DPAdmin(admin.ModelAdmin):
    list_display = ('nom', 'modelo','serie')
