from django.db import migrations
from django.utils.text import slugify

def generar_slugs(apps, schema_editor):
    Mascota = apps.get_model('mascota', 'Mascota')
    for mascota in Mascota.objects.all():
        if not mascota.slug:
            base_slug = slugify(mascota.nombre)
            slug = base_slug
            counter = 1
            
            # Asegura que el slug sea único
            existing_slugs = [m.slug for m in Mascota.objects.all() if m.slug]
            while slug in existing_slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            mascota.slug = slug
            mascota.save(update_fields=['slug'])

def revertir_slugs(apps, schema_editor):
    # No hacemos nada en la reversión
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('mascota', '0008_add_mascota_slug'),  # Asegúrate de que este nombre coincida con la migración anterior
    ]

    operations = [
        migrations.RunPython(generar_slugs, revertir_slugs),
    ]
