from django.contrib import admin

from .models import Pagina


@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "fecha_publicacion", "destacada")
    list_filter = ("fecha_publicacion", "destacada")
    search_fields = ("titulo", "extracto", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "fecha_publicacion"
