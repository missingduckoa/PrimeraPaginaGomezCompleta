from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField

User = get_user_model()


class TipoMascota(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('adoptado', 'Adoptado'),
        ('en_proceso', 'En proceso de adopción'),
    ]

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    tipo = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField(help_text="Edad en meses")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='mascotas/', null=True, blank=True,
                           help_text="Imagen principal (opcional si se suben otras imágenes)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    publicado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas_publicadas')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True, help_text="Ciudad donde está la mascota")
    region = models.CharField(max_length=100, null=True, blank=True, help_text="Región/Provincia/Estado")
    codigo_postal = models.CharField(max_length=10, null=True, blank=True, help_text="Código postal (opcional)")

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Genera un slug único basado en el nombre
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            
            # Asegura que el slug sea único
            while Mascota.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mascota:detalle_mascota', kwargs={'slug': self.slug})

    def get_imagen_principal(self):
        """Retorna la imagen principal, ya sea la primera de la colección o el campo 'foto'"""
        imagen_principal = self.imagenes.filter(es_principal=True).first()
        if imagen_principal:
            return imagen_principal.imagen

        # Si no hay imagen principal en la colección, usa el campo foto tradicional
        return self.foto

class ImagenMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='mascotas/')
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Mascota'
        verbose_name_plural = 'Imágenes de Mascotas'

    def __str__(self):
        return f"Imagen {self.orden} de {self.mascota.nombre}"

class SolicitudAdopcion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    motivo = models.TextField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.solicitante.username} para {self.mascota.nombre}"


# Modelos para el blog
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    contenido = models.TextField()
    resumen = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='blog/', null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, related_name='articulos')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articulos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True, null=True, help_text="Incluye el código de país, ejemplo: +56912345678")
    whatsapp = models.BooleanField(default=True, help_text="¿Desea ser contactado por WhatsApp?")
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea un perfil cuando se crea un nuevo usuario"""
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, created, **kwargs):
    """Actualiza el perfil cuando se actualiza el usuario"""
    # Solo intentamos guardar el perfil si no es una creación nueva
    # para evitar recursión infinita
    if not created:
        try:
            if hasattr(instance, 'perfil'):
                instance.perfil.save()
        except Exception:
            # Si hay cualquier error, creamos un nuevo perfil
            Perfil.objects.create(usuario=instance)
        
class Notificacion(models.Model):
    TIPOS = (
        ('solicitud', 'Solicitud de adopción'),
        ('aprobada', 'Solicitud aprobada'),
        ('rechazada', 'Solicitud rechazada'),
        ('sistema', 'Notificación del sistema'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enlace = models.CharField(max_length=255, blank=True, null=True)  # URL relacionada con la notificación
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.mensaje[:30]}..."
    
    @staticmethod
    def no_leidas_count(usuario):
        """Cuenta las notificaciones no leídas de un usuario"""
        return Notificacion.objects.filter(usuario=usuario, leida=False).count()

# Función para crear notificaciones
def crear_notificacion(usuario, tipo, mensaje, enlace=None):
    return Notificacion.objects.create(
        usuario=usuario,
        tipo=tipo,
        mensaje=mensaje,
        enlace=enlace
    )

class Blog(models.Model):
    title = models.CharField(max_length=200)  # Título del blog
    subtitle = models.CharField(max_length=200, blank=True, null=True)  # Subtítulo opcional
    content = RichTextField()  # Contenido del blog
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)  # Imagen opcional
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor del blog
    categories = models.ManyToManyField('Category', related_name='blogs', blank=True)  # Categorías opcionales

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name