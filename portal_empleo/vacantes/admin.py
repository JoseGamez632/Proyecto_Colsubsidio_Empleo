from django.contrib import admin
from .models import Vacante, RegistroCandidato, Departamento, Ciudad
# Register your models here.




class VacanteAdmin(admin.ModelAdmin):
    list_display = ('codigo_vacante', 'cargo', 'area', 'ver_candidatos')  # Añade ver_candidatos

    def ver_candidatos(self, obj):
        """Devuelve un enlace para ver candidatos asociados."""
        url = f"/admin/app_name/registrocandidato/?vacantes_disponibles__id__exact={obj.id}"
        return f'<a href="{url}" target="_blank">Ver Candidatos</a>'

    ver_candidatos.allow_tags = True  # Permite que el HTML se renderice correctamente
    ver_candidatos.short_description = "Candidatos"  # Texto en la cabecera de la columna
    
class RegistroCandidatoAdmin(admin.ModelAdmin):
    list_filter = ('vacantes_disponibles',)  # Filtra por las vacantes asociadas

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)  # Muestra solo el nombre en la lista
    search_fields = ("nombre",)  # Permite buscar por nombre

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento")  # Muestra nombre y su departamento
    search_fields = ("nombre", "departamento__nombre")  # Permite buscar por nombre de ciudad o departamento
    list_filter = ("departamento",)  # Agrega un filtro por departamento en la barra lateral



admin.site.register(Vacante, VacanteAdmin)
admin.site.register(RegistroCandidato, RegistroCandidatoAdmin)