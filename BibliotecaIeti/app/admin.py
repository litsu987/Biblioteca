from django.contrib import admin
from .models import Centre, Cicle, TipusMaterial, Usuari, Catalog, ElementCatalog, Exemplar, Reserva, Prestec, Peticio, Log, ImatgeCatalog

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
    list_display = ('user', 'data_naixement', 'centre', 'cicle', 'imatge','email','nom','cognoms')

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('nom', 'descripcio')

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
    list_display = ('usuari', 'accio', 'data_accio')

@admin.register(ImatgeCatalog)
class ImatgeCatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'imatge')
