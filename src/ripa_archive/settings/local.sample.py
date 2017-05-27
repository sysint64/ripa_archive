from ripa_archive.settings.base import *

VAR_ROOT = os.path.join(BASE_DIR, '../../var')
FRONTEND_ROOT = os.path.join(BASE_DIR, '../../frontend')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'media')


DEBUG = True
SECRET_KEY = 'demo'

ALLOWED_HOSTS = [
    "*"
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'db.sqlite3'),
    }
}

LOCALE_PATHS = (
    os.path.join(VAR_ROOT, 'locale'),
)

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', "sassc"+' --style compressed {infile} {outfile}'),
)
