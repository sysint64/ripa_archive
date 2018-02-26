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
    ('text/x-sass', "sassc --style compressed {infile} {outfile}"),
    ('text/x-scss', "sassc --style compressed {infile} {outfile}"),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(FRONTEND_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ripa_archive.context_processors.search',
                'ripa_archive.context_processors.common',
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(FRONTEND_ROOT, 'static'),
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:9001/solr/ripa_archive',
        'INCLUDE_SPELLING': True,
    },
}
