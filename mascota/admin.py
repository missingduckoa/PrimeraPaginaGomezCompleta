from django.contrib import admin
from .models import TipoMascota, Mascota, SolicitudAdopcion, Categoria, Articulo, Blog, Category

@admin.register(TipoMascota)
class TipoMascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'raza', 'edad', 'sexo', 'estado', 'publicado_por', 'fecha_publicacion')
    list_filter = ('tipo', 'sexo', 'estado')
    search_fields = ('nombre', 'raza', 'descripcion')
    date_hierarchy = 'fecha_publicacion'

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'solicitante', 'estado', 'fecha_solicitud')
    list_filter = ('estado',)
    search_fields = ('mascota__nombre', 'solicitante__username')
    date_hierarchy = 'fecha_solicitud'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion', 'publicado', 'destacado')
    list_filter = ('publicado', 'destacado', 'categorias', 'fecha_creacion')
    search_fields = ('titulo', 'contenido', 'autor__username')
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ('categorias',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fecha_creacion'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('categories', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}