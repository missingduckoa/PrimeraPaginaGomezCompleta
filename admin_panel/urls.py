from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('publicaciones/', views.listar_publicaciones, name='listar_publicaciones'),
    path('publicaciones/eliminar/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('reportes/', views.listar_reportes, name='listar_reportes'),
    path('reportes/marcar-revisado/<int:reporte_id>/', views.marcar_reporte_revisado, name='marcar_reporte_revisado'),
]