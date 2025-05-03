# PrimeraPaginaGomezCompleta

## Descripción
Este es un proyecto web desarrollado en Django que incluye herencia de plantillas, modelos y formularios. Aunque originalmente debía ser un blog (según entendí, esto era opcional), decidí enfocarlo en una página web cuyo objetivo es facilitar la adopción, publicación y solicitud de mascotas.

---

## Cómo probar el proyecto

1. **Clona el repositorio:**
   Abre GitBash o la terminal de tu preferencia y ejecuta:
   ```bash
   git clone https://github.com/missingduckoa/PrimeraPaginaGomezCompleta.git
2. **Crea y activa el entorno virtual:**

Para crear el entorno virtual:
python -m venv env

3. **Instala las dependencias: Ejecuta el siguiente comando para instalar las dependencias necesarias:**
pip install -r requirements.txt

5. **Antes de correr el servidor, asegurate de aplicar correctamente las migraciones:**
python manage.py migrate

7. **Corre el servidor:**
python manage.py runserver

9. **Accede a la web con el siguiente link:**
http://127.0.0.1:8000/

***Pruebe las funcionalidades del proyecto***
Usa los botones de la página para:

- Adoptar mascotas.
- Publicar mascotas en adopción.
- Solicitar adopciones.
- Navegar por el blog y leer artículos relacionados con el cuidado de mascotas.

##Proyecto realizado por: Sofía Gómez

#Notas importantes
No se incluye el archivo db.sqlite3 en el repositorio. Si necesitas datos de prueba, crea tu propia base de datos ejecutando las migraciones.
Las imágenes subidas por los usuarios no están incluidas en el repositorio. Estas se almacenan en la carpeta media, que está excluida en el archivo .gitignore.
El diseño visual es básico. Se priorizó la funcionalidad sobre la apariencia.
