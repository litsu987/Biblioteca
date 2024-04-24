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
    list_display = ('email', 'nom', 'data_naixement', 'centre', 'cicle', 'imatge')

    def mostrar_centro(self, obj):
        return obj.centre.nom if obj.centre else ""
    mostrar_centro.short_description = 'Centre'

    def mostrar_cicle(self, obj):
        return obj.cicle.nom if obj.cicle else ""
    mostrar_cicle.short_description = 'Cicle'


@admin.register(ElementCatalog)
class ElementCatalogAdmin(admin.ModelAdmin):
    list_display = ('get_catalog_name', 'get_tipus_material_name')

    def get_catalog_name(self, obj):
        return obj.catalog.nom
    get_catalog_name.short_description = 'Catalog'

    def get_tipus_material_name(self, obj):
        return obj.tipus_material.nom
    get_tipus_material_name.short_description = 'Tipus Material'


@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('element_catalog', 'estat')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'get_element_titulo', 'data_reserva')

   
    def get_element_titulo(self, obj):
        return obj.exemplar.element_catalog.catalog.nom
    get_element_titulo.short_description = 'Element Títol'


@admin.register(Prestec)
class PrestecAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'get_element_titulo', 'data_prestec', 'data_retorn')

 

    def get_element_titulo(self, obj):
        return obj.exemplar.element_catalog.catalog.nom
    get_element_titulo.short_description = 'Element Títol'


@admin.register(Peticio)
class PeticioAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'titol_peticio', 'descripcio', 'data_peticio')



@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'accio', 'data_accio', 'tipus')
    list_display = ('usuari', 'accio', 'data_accio', 'tipus')

@admin.register(ImatgeCatalog)
class ImatgeCatalogAdmin(admin.ModelAdmin):
    list_display = ('get_catalog_name', 'imatge')

    def get_catalog_name(self, obj):
        return obj.catalog.nom
    get_catalog_name.short_description = 'Catálogo'


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
