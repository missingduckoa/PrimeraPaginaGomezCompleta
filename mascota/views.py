from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Mascota, SolicitudAdopcion, TipoMascota, ImagenMascota, Notificacion, crear_notificacion
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import MascotaForm, SolicitudAdopcionForm, FormularioContacto, CustomUserCreationForm, CustomAuthenticationForm, PerfilForm
from admin_panel.models import Reporte
from .models import Blog, Category  # Importa el modelo Blog y Category

def home(request):
    mascotas_recientes = Mascota.objects.filter(estado='disponible').order_by('-fecha_publicacion')[:4]
    return render(request, 'mascota/home.html', {
        'mascotas_recientes': mascotas_recientes
    })


def lista_mascotas(request):
    mascotas = Mascota.objects.filter(estado='disponible').order_by('-fecha_publicacion')
    tipos = TipoMascota.objects.all()

    tipo_id = request.GET.get('tipo')
    if tipo_id:
        mascotas = mascotas.filter(tipo_id=tipo_id)

    return render(request, 'mascota/lista_mascotas.html', {
        'mascotas': mascotas,
        'tipos': tipos
    })


def detalle_mascota(request, slug):
    mascota = get_object_or_404(Mascota, slug=slug)
    return render(request, 'mascota/detalle_mascota.html', {
        'mascota': mascota
    })


def detalle_mascota_legacy(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return redirect(mascota.get_absolute_url(), permanent=True)


@login_required
def publicar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.publicado_por = request.user
            mascota.save()
            
            # Procesar la foto principal
            if mascota.foto:
                # Crear una entrada en ImagenMascota para la foto principal
                ImagenMascota.objects.create(
                    mascota=mascota,
                    imagen=mascota.foto,
                    es_principal=True,
                    orden=0
                )
            
            # Procesar imágenes adicionales
            files = request.FILES.getlist('imagenes_adicionales')
            for i, img in enumerate(files, 1):  # Comienza desde 1 porque la principal es 0
                ImagenMascota.objects.create(
                    mascota=mascota,
                    imagen=img,
                    orden=i
                )
            
            messages.success(request, 'Mascota publicada correctamente')
            return redirect('mascota:detalle_mascota', slug=mascota.slug)
    else:
        form = MascotaForm()

    return render(request, 'mascota/publicar_mascota.html', {
        'form': form
    })


@login_required
def solicitar_adopcion(request, slug):
    mascota = get_object_or_404(Mascota, slug=slug)

    # Verificar que la mascota esté disponible
    if mascota.estado != 'disponible':
        messages.error(request, f'Esta mascota ya no está disponible para adopción 🐶')
        return redirect('mascota:detalle_mascota', slug=mascota.slug)

    # Verificar que el usuario no sea el que publicó la mascota
    if mascota.publicado_por == request.user:
        messages.error(request, f'No puedes solicitar adoptar una mascota que tú mismo publicaste')
        return redirect('mascota:detalle_mascota', slug=mascota.slug)

    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.mascota = mascota
            solicitud.solicitante = request.user
            solicitud.save()

            # Cambiar estado de la mascota
            mascota.estado = 'en_proceso'
            mascota.save()

            # Crear notificación para el dueño de la mascota
            crear_notificacion(
                usuario=mascota.publicado_por,
                tipo='solicitud',
                mensaje=f'{request.user.username} ha solicitado adoptar a {mascota.nombre}.',
                enlace=reverse('mascota:mis_publicaciones')
            )

            # Enviar correo al usuario que publicó la mascota
            try:
                send_mail(
                    subject=f'Nueva solicitud de adopción para {mascota.nombre}',
                    message=(
                        f'Hola, {mascota.publicado_por.username},\n\n'
                        f'Hemos recibido una nueva solicitud de adopción para {mascota.nombre}.\n'
                        f'Solicitante: {solicitud.solicitante.username}\n'
                        f'Motivo: {solicitud.motivo}\n'
                        f'Dirección: {solicitud.direccion}\n'
                        f'Teléfono: {solicitud.telefono}\n\n'
                        f'Revisa las solicitudes en tu perfil. ¡Gracias por usar Mascoteros! 🐶'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[mascota.publicado_por.email],
                    fail_silently=False,
                )
                messages.success(request, f'Solicitud enviada correctamente')
            except Exception as e:
                messages.error(request, f'Solicitud guardada, pero hubo un error al enviar el correo: {str(e)}')

            return redirect('mascota:detalle_mascota', slug=mascota.slug)
    else:
        form = SolicitudAdopcionForm()

    return render(request, 'mascota/solicitar_adopcion.html', {
        'form': form,
        'mascota': mascota
    })


@login_required
def solicitar_adopcion_legacy(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    return redirect('mascota:solicitar_adopcion', slug=mascota.slug, permanent=True)


@login_required
def mis_publicaciones(request):
    mascotas = Mascota.objects.filter(publicado_por=request.user).order_by('-fecha_publicacion')
    return render(request, 'mascota/mis_publicaciones.html', {
        'mascotas': mascotas
    })


@login_required
def mis_solicitudes(request):
    solicitudes = SolicitudAdopcion.objects.filter(solicitante=request.user).order_by('-fecha_solicitud')
    return render(request, 'mascota/mis_solicitudes.html', {
        'solicitudes': solicitudes
    })


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                send_mail(
                    subject=f'¡Bienvenido a Mascoteros, {user.username}! 🐶',
                    message=(
                        f'Hola, {user.username},\n\n'
                        f'Gracias por registrarte en Mascoteros. ¡Ahora puedes publicar mascotas para adopción, '
                        f'solicitar adoptar, y mucho más!\n\n'
                        f'Si tienes alguna pregunta, contáctanos en {settings.DEFAULT_FROM_EMAIL}.\n\n'
                        f'¡Esperamos que encuentres a tu nuevo mejor amigo! 🐶'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Registro exitoso')
            except Exception as e:
                messages.warning(request, f'Registro exitoso, pero hubo un error al enviar el correo de bienvenida: {str(e)}')
            return redirect('mascota:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'mascota/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido/a {username}')
                return redirect('mascota:home')
    else:
        form = CustomAuthenticationForm(request)  # Aquí está el cambio: pasar request como argumento

    return render(request, 'mascota/login.html', {
        'form': form
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('mascota:home')


# Funciones del blog
def blog_lista(request):
    # Por ahora, una implementación temporal mientras defines los modelos
    return render(request, 'mascota/blog/lista.html', {
        'articulos': [],
        'categorias': []
    })


def blog_detalle(request, slug):
    # Implementación temporal
    return render(request, 'mascota/blog/detalle.html', {
        'articulo': None
    })


def blog_por_categoria(request, categoria_slug):
    # Implementación temporal
    return render(request, 'mascota/blog/lista.html', {
        'articulos': [],
        'categorias': [],
        'categoria_actual': categoria_slug
    })


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'mascota/blog/detalle.html'
    context_object_name = 'articulo'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'subtitle', 'content', 'image', 'categories']
    template_name = 'mascota/blog/formulario.html'
    success_url = reverse_lazy('mascota:blog_lista')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'subtitle', 'content', 'image', 'categories']
    template_name = 'mascota/blog/formulario.html'
    success_url = reverse_lazy('mascota:blog_lista')


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'mascota/blog/confirmar_eliminar.html'
    success_url = reverse_lazy('mascota:blog_lista')


class BlogCategoryView(ListView):
    model = Blog
    template_name = 'mascota/blog/lista.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        # Filtra los artículos por la categoría seleccionada
        categoria_slug = self.kwargs.get('slug')
        return Blog.objects.filter(categories__slug=categoria_slug)

    def get_context_data(self, **kwargs):
        # Agrega las categorías al contexto
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['categoria_actual'] = self.kwargs.get('slug')
        return context


@login_required
def editar_mascota(request, slug):
    mascota = get_object_or_404(Mascota, slug=slug)

    # Verificar que el usuario sea el propietario de la mascota
    if mascota.publicado_por != request.user:
        messages.error(request, 'No tienes permiso para editar esta mascota')
        return redirect('mascota:mis_publicaciones')

    if mascota.estado == 'adoptado':
        messages.error(request, 'No se puede editar una mascota que ya ha sido adoptada')
        return redirect('mascota:mis_publicaciones')

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            mascota = form.save()
            
            # Procesar imágenes adicionales nuevas
            files = request.FILES.getlist('imagenes_adicionales')
            if files:
                # Obtener el último orden de imagen existente
                ultimo_orden = ImagenMascota.objects.filter(mascota=mascota).order_by('-orden').first()
                orden_inicial = 0 if not ultimo_orden else ultimo_orden.orden + 1
                
                # Guardar las nuevas imágenes
                for i, img in enumerate(files, orden_inicial):
                    ImagenMascota.objects.create(
                        mascota=mascota,
                        imagen=img,
                        orden=i
                    )
            
            messages.success(request, 'Mascota actualizada correctamente')
            return redirect('mascota:detalle_mascota', slug=mascota.slug)
    else:
        form = MascotaForm(instance=mascota)

    # Obtener las imágenes existentes
    imagenes = ImagenMascota.objects.filter(mascota=mascota).order_by('orden')
    
    return render(request, 'mascota/editar_mascota.html', {
        'form': form,
        'mascota': mascota,
        'imagenes': imagenes
    })


@login_required
def editar_mascota_legacy(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return redirect('mascota:editar_mascota', slug=mascota.slug, permanent=True)


@login_required
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudAdopcion, pk=solicitud_id)

    # Verificar que el usuario sea el solicitante
    if solicitud.solicitante != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta solicitud')
        return redirect('mascota:mis_solicitudes')

    # Solo permitir eliminar solicitudes pendientes
    if solicitud.estado != 'pendiente':
        messages.error(request, 'No se puede eliminar una solicitud que ya ha sido procesada')
        return redirect('mascota:mis_solicitudes')

    # Obtener la mascota para actualizar su estado
    mascota = solicitud.mascota

    if request.method == 'POST':
        # Eliminar la solicitud
        solicitud.delete()

        # Verificar si hay otras solicitudes pendientes para esta mascota
        otras_solicitudes = SolicitudAdopcion.objects.filter(mascota=mascota, estado='pendiente').exists()

        # Si no hay otras solicitudes, cambiar el estado de la mascota a 'disponible'
        if not otras_solicitudes and mascota.estado == 'en_proceso':
            mascota.estado = 'disponible'
            mascota.save()

        messages.success(request, 'Solicitud eliminada correctamente')
        return redirect('mascota:mis_solicitudes')

    return render(request, 'mascota/eliminar_solicitud.html', {
        'solicitud': solicitud
    })


@login_required
def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(ImagenMascota, pk=imagen_id)
    mascota = imagen.mascota
    
    # Verificar que el usuario sea el propietario de la mascota
    if mascota.publicado_por != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta imagen')
        return redirect('mascota:mis_publicaciones')
    
    if request.method == 'POST':
        # Guardar información para mensajes
        es_principal = imagen.es_principal
        
        # Eliminar la imagen
        imagen.delete()
        
        # Si era la principal, asignar una nueva imagen principal
        if es_principal:
            nueva_principal = ImagenMascota.objects.filter(mascota=mascota).first()
            if nueva_principal:
                nueva_principal.es_principal = True
                nueva_principal.save()
        
        messages.success(request, 'Imagen eliminada correctamente')
        return redirect('mascota:editar_mascota', slug=mascota.slug)
    
    return render(request, 'mascota/eliminar_imagen.html', {
        'imagen': imagen,
        'mascota': mascota
    })


@login_required
def establecer_imagen_principal(request, imagen_id):
    imagen = get_object_or_404(ImagenMascota, pk=imagen_id)
    mascota = imagen.mascota
    
    # Verificar que el usuario sea el propietario de la mascota
    if mascota.publicado_por != request.user:
        messages.error(request, 'No tienes permiso para modificar esta mascota')
        return redirect('mascota:mis_publicaciones')
    
    # Quitar el estado principal de todas las imágenes de la mascota
    ImagenMascota.objects.filter(mascota=mascota, es_principal=True).update(es_principal=False)
    
    # Establecer esta imagen como principal
    imagen.es_principal = True
    imagen.save()
    
    messages.success(request, 'Imagen establecida como principal')
    return redirect('mascota:editar_mascota', slug=mascota.slug)


def contacto(request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            try:
                send_mail(
                    subject=f'Mensaje de contacto de {nombre}',
                    message=f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['mascoteronet@gmail.com'],  # Correo destino
                    fail_silently=False,
                )
                messages.success(request, 'Mensaje enviado correctamente. Gracias por contactarnos.')
                return redirect('mascota:home')  # Redirecciona a la página principal
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {str(e)}')
    else:
        form = FormularioContacto()
    return render(request, 'contacto.html', {'form': form})  # Corrige la ruta a tu plantilla
    
def nosotros(request):
    return render(request, 'nosotros.html')  # Sin el prefijo 'mascota/'
    

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user.perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('mascota:home')  # O donde prefieras redirigir
    else:
        form = PerfilForm(instance=request.user.perfil)
    
    return render(request, 'mascota/editar_perfil.html', {
        'form': form
    })


@login_required
def reportar_mascota(request, slug):
    mascota = get_object_or_404(Mascota, slug=slug)
    
    # No permitir reportar las propias mascotas
    if request.user == mascota.publicado_por:
        messages.error(request, "No puedes reportar tus propias publicaciones.")
        return redirect('mascota:detalle_mascota', slug=slug)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        descripcion = request.POST.get('descripcion', '')
        
        # Verificar si ya existe un reporte de este usuario para esta mascota
        reporte_existente = Reporte.objects.filter(
            mascota=mascota,
            usuario_reportador=request.user,
            revisado=False
        ).exists()
        
        if reporte_existente:
            messages.warning(request, "Ya has reportado esta publicación anteriormente.")
        else:
            Reporte.objects.create(
                mascota=mascota,
                usuario_reportador=request.user,
                motivo=motivo,
                descripcion=descripcion
            )
            messages.success(request, "Reporte enviado correctamente. Gracias por ayudarnos a mantener la plataforma segura.")
        
    return redirect('mascota:detalle_mascota', slug=slug)


@login_required
def reportar_mascota_legacy(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return redirect('mascota:reportar_mascota', slug=mascota.slug, permanent=True)


# Nuevas vistas para el sistema de notificaciones
@login_required
def mis_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    no_leidas_count = notificaciones.filter(leida=False).count()
    return render(request, 'mascota/mis_notificaciones.html', {
        'notificaciones': notificaciones,
        'no_leidas_count': no_leidas_count
    })

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    
    if notificacion.enlace:
        return redirect(notificacion.enlace)
    
    return redirect('mascota:mis_notificaciones')

@login_required
def marcar_todas_leidas(request):
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    return redirect('mascota:mis_notificaciones')