from django import template
from mascota.models import Notificacion

register = template.Library()

@register.simple_tag
def notificaciones_no_leidas(usuario):
    """Devuelve el número de notificaciones no leídas del usuario"""
    if usuario.is_authenticated:
        return Notificacion.objects.filter(usuario=usuario, leida=False).count()
    return 0

@register.filter
def no_leidas_count(notificaciones):
    """Filtra las notificaciones no leídas"""
    return notificaciones.filter(leida=False).count()