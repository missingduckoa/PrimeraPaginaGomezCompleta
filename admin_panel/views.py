from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from mascota.models import Mascota
from .models import Reporte

User = get_user_model()

# Verificación de administrador
def es_admin(user):
    return user.is_authenticated and user.is_staff

# Vista del dashboard
@user_passes_test(es_admin)
def dashboard(request):
    total_mascotas = Mascota.objects.count()
    total_usuarios = User.objects.count()
    reportes_pendientes = Reporte.objects.filter(revisado=False).count()
    
    # Datos para gráficos
    
    # Mascotas por tipo
    mascotas_por_tipo = Mascota.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('tipo')
    
    # Convertir a formato para Chart.js
    tipos = [item['tipo'] for item in mascotas_por_tipo]
    totales = [item['total'] for item in mascotas_por_tipo]
    
    # Publicaciones por mes
    publicaciones_por_mes = Mascota.objects.annotate(
        mes=TruncMonth('fecha_publicacion')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Convertir a formato para Chart.js
    meses = [item['mes'].strftime('%b %Y') for item in publicaciones_por_mes]
    totales_mes = [item['total'] for item in publicaciones_por_mes]
    
    return render(request, 'admin_panel/dashboard.html', {
        'total_mascotas': total_mascotas,
        'total_usuarios': total_usuarios,
        'reportes_pendientes': reportes_pendientes,
        'tipos_json': json.dumps(tipos),
        'totales_json': json.dumps(totales),
        'meses_json': json.dumps(meses),
        'totales_mes_json': json.dumps(totales_mes),
        'active_tab': 'dashboard',
    })

# Vista para listar publicaciones
@user_passes_test(es_admin)
def listar_publicaciones(request):
    publicaciones_list = Mascota.objects.all().order_by('-fecha_publicacion')
    
    # Aplicamos filtros si existen
    tipo = request.GET.get('tipo')
    if tipo:
        publicaciones_list = publicaciones_list.filter(tipo=tipo)
    
    estado = request.GET.get('estado')
    if estado:
        publicaciones_list = publicaciones_list.filter(estado=estado)
    
    # Paginación
    paginator = Paginator(publicaciones_list, 10)  # 10 elementos por página
    page = request.GET.get('page')
    
    try:
        publicaciones = paginator.page(page)
    except PageNotAnInteger:
        publicaciones = paginator.page(1)
    except EmptyPage:
        publicaciones = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/publicaciones.html', {
        'publicaciones': publicaciones,
        'active_tab': 'publicaciones',
    })

# Vista para eliminar publicación
@user_passes_test(es_admin)
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Mascota, id=publicacion_id)
    
    if request.method == 'POST':
        nombre = publicacion.nombre  # Guardamos el nombre antes de eliminar
        publicacion.delete()
        messages.success(request, f"La publicación '{nombre}' ha sido eliminada con éxito.")
        return redirect('admin_panel:listar_publicaciones')
    
    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': publicacion,
        'tipo': 'publicación',
        'active_tab': 'publicaciones',
    })

# Vista para listar usuarios
@user_passes_test(es_admin)
def listar_usuarios(request):
    usuarios_list = User.objects.all().order_by('-date_joined')
    
    # Paginación
    paginator = Paginator(usuarios_list, 10)  # 10 elementos por página
    page = request.GET.get('page')
    
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/usuarios.html', {
        'usuarios': usuarios,
        'active_tab': 'usuarios',
    })

# Vista para eliminar usuario
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        username = usuario.username  # Guardamos el nombre antes de eliminar
        
        # No permitimos eliminar al propio admin que está logueado
        if request.user == usuario:
            messages.error(request, "No puedes eliminar tu propio usuario.")
            return redirect('admin_panel:listar_usuarios')
        
        usuario.delete()
        messages.success(request, f"El usuario '{username}' ha sido eliminado con éxito.")
        return redirect('admin_panel:listar_usuarios')
    
    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': usuario,
        'tipo': 'usuario',
        'active_tab': 'usuarios',
    })

# Vista para listar reportes
@user_passes_test(es_admin)
def listar_reportes(request):
    reportes_list = Reporte.objects.all().order_by('-fecha_reporte')
    
    # Paginación
    paginator = Paginator(reportes_list, 10)  # 10 elementos por página
    page = request.GET.get('page')
    
    try:
        reportes = paginator.page(page)
    except PageNotAnInteger:
        reportes = paginator.page(1)
    except EmptyPage:
        reportes = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/reportes.html', {
        'reportes': reportes,
        'active_tab': 'reportes',
    })

# Vista para marcar reporte como revisado
@user_passes_test(es_admin)
def marcar_reporte_revisado(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    reporte.revisado = True
    reporte.save()
    
    messages.success(request, "Reporte marcado como revisado.")
    return redirect('admin_panel:listar_reportes')