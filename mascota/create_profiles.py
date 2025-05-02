# En un nuevo archivo llamado create_profiles.py en la carpeta de tu aplicación
from django.contrib.auth.models import User
from mascota.models import Perfil

def run():
    users = User.objects.all()
    for user in users:
        try:
            # Si el usuario ya tiene perfil, saltarlo
            user.perfil
        except:
            # Si no tiene perfil, crear uno
            print(f"Creando perfil para {user.username}")
            Perfil.objects.create(usuario=user)