# config/settings.py
import os
from dotenv import load_dotenv
load_dotenv()
import dj_database_url
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'H42YRVtHh-6RwbKk2ZEovXLIoOu8IZYMCTc1nEYjWSn2RehgYGtGQWRO4zEk8Vq3T0U')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.mascoteros.net']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'mascota',  # Tu aplicación
    'admin_panel',  # nueva app de administración
    'ckeditor',
    'ckeditor_uploader',  # Solo si usarás la carga de imágenes
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Descomentado ahora que has instalado whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configura BD para producción si DATABASE_URL está disponible
if os.environ.get('DATABASE_URL'):
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'  # Ajusta a tu zona horaria
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cambiado a una versión más simple para depuración
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL
LOGIN_URL = 'mascota:login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'  # Usa el Postfix local
EMAIL_PORT = 25  # Puerto local de Postfix
EMAIL_USE_TLS = False  # No necesitas TLS para conexión local
EMAIL_HOST_USER = ''  # No necesitas autenticación local
EMAIL_HOST_PASSWORD = ''  # No necesitas contraseña local
DEFAULT_FROM_EMAIL = 'maurozx27@gmail.com'  # Cambia a tu dominio

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587  # Puerto para TLS
# EMAIL_USE_TLS = True  # Activa TLS
# EMAIL_USE_SSL = False  # Desactiva SSL (no necesario con TLS)
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER', 'maurozx27@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'rdxb rjvv ckib hdrl')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Configuración de CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"  # Carpeta donde se guardarán las imágenes subidas