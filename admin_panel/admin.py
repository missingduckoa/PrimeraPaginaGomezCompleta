from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'usuario_reportador', 'motivo', 'fecha_reporte', 'revisado')
    list_filter = ('motivo', 'revisado')
    search_fields = ('mascota__nombre', 'usuario_reportador__username')
    date_hierarchy = 'fecha_reporte'