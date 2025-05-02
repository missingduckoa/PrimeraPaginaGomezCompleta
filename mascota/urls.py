# mascota/urls.py
from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'mascota'

urlpatterns = [
    # URLs principales
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),

    # URLs de mascotas
    path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/nueva/', views.publicar_mascota, name='publicar_mascota'),  # Ruta específica
    path('mascotas/<slug:slug>/', views.detalle_mascota, name='detalle_mascota'),  # Ruta general
    path('mascotas/<slug:slug>/editar/', views.editar_mascota, name='editar_mascota'),
    path('mascota/<slug:slug>/reportar/', views.reportar_mascota, name='reportar_mascota'),

    # URLs de solicitudes
    path('solicitud/<slug:slug>/', views.solicitar_adopcion, name='solicitar_adopcion'),
    path('solicitud/<int:solicitud_id>/eliminar/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),

    # URLs de publicaciones
    path('mis-publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),

    # URLs de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # URLs del blog
    path('blog/', views.blog_lista, name='blog_lista'),
    path('blog/<slug:slug>/', views.blog_detalle, name='blog_detalle'),
    path('blog/categoria/<slug:categoria_slug>/', views.blog_por_categoria, name='blog_categoria'),

    # URLs de notificaciones
    path('notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/marcar-todas-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),

    # Redirecciones de URLs antiguas para mantener compatibilidad
    path('mascotas/<int:pk>/', views.detalle_mascota_legacy, name='detalle_mascota_legacy'),
    path('mascotas/<int:pk>/editar/', views.editar_mascota_legacy, name='editar_mascota_legacy'),
    path('solicitud/<int:mascota_id>/', views.solicitar_adopcion_legacy, name='solicitar_adopcion_legacy'),
    path('mascota/<int:pk>/reportar/', views.reportar_mascota_legacy, name='reportar_mascota_legacy'),

    # Archivo robots.txt
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]