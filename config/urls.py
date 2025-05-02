from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from mascota.sitemaps import MascotaSitemap, StaticViewSitemap

sitemaps = {
    'mascotas': MascotaSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # Añadir esta línea para incluir el panel de administración personalizado
    path('admin_panel/', include('admin_panel.urls')),
    path('', include('mascota.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Para servir archivos multimedia durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
