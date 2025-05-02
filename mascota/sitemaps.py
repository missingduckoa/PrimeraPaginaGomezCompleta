from django.contrib.sitemaps import Sitemap
from .models import Mascota, Articulo
from django.urls import reverse

class MascotaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Mascota.objects.filter(estado='disponible')

    def lastmod(self, obj):
        return obj.fecha_publicacion
        
    def location(self, obj):
        return reverse('mascota:detalle_mascota', args=[obj.pk])

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ['mascota:home', 'mascota:lista_mascotas', 'mascota:contacto', 'mascota:nosotros']

    def location(self, item):
        return reverse(item)
