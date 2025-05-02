from django.db import models
from django.contrib.auth import get_user_model
from mascota.models import Mascota

User = get_user_model()

class Reporte(models.Model):
    MOTIVOS = (
        ('spam', 'Contenido spam o engañoso'),
        ('ofensivo', 'Contenido ofensivo'),
        ('duplicado', 'Publicación duplicada'),
        ('otro', 'Otro motivo'),
    )
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='reportes')
    usuario_reportador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes_realizados')
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    revisado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reporte de {self.mascota.nombre} por {self.usuario_reportador.username}"