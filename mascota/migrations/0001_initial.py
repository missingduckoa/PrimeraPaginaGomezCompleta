# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoMascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('raza', models.CharField(max_length=100)),
                ('edad', models.IntegerField(help_text='Edad en meses')),
                ('sexo', models.CharField(choices=[('M', 'Macho'), ('H', 'Hembra')], max_length=1)),
                ('descripcion', models.TextField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='mascotas/')),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('adoptado', 'Adoptado'), ('en_proceso', 'En proceso de adopción')], default='disponible', max_length=20)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('publicado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascotas_publicadas', to=settings.AUTH_USER_MODEL)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.tipomascota')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudAdopcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.TextField()),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=15)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=20)),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.mascota')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
