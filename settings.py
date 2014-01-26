# -*- coding: utf-8 -*-
# Django settings for clubeoferta project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
     ('Fernando Freitas Alves', 'ffreitasalves@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'clubeoferta.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'
DATETIME_INPUT_FORMATS= ('%d/%m/%Y %H:%M:%S',)
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
SHORT_DATE_FORMAT = 'd/m/Y'
E_MAIL_COBRANCA = ""
TOKEN = ''

#Configurações de E-mail
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_PORT = 587
EMAIL_USE_TLS=True
SERVER_EMAIL = ""

#Informação sobre a sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE	 = True
SESSION_COOKIE_AGE = 900

#Extensão do módulo de usuários
AUTH_PROFILE_MODULE = 'cadastro.usuarios'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://localhost:8000/media/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z2!9+131tv*qp_8_qhaq*%&0i6%c7o7kqdilhc8^!$#yg!m!m('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'clubeoferta.urls'

TEMPLATE_DIRS = (
    ( os.path.join(SITE_ROOT, 'html'),)
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
'django.core.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.comments',

    'clubeoferta.anuncio',
    'clubeoferta.cadastro',
    'clubeoferta.compra',
    'clubeoferta.divulgacao',
    'clubeoferta.pagseguropy',
    
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/conta/'
