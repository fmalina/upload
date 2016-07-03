import os

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True
THUMBNAIL_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'upload.db',
    }
}
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = APP_ROOT + STATIC_URL
MEDIA_ROOT = STATIC_ROOT + 'media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # auth
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)
ROOT_URLCONF = 'upload.tests.test_urls'
INSTALLED_APPS = (
    'upload',
    'easy_thumbnails',
    'django.contrib.staticfiles',

    # auth (for user uploaded collections)
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
)
THUMBNAIL_ALIASES = {
    '': {
        'large':  {'size': (400, 400), 'crop': True},
        'medium': {'size': (180, 180), 'crop': True},
        'small':  {'size': (100, 100), 'crop': True},
        'tiny':   {'size': (50, 50),   'crop': True},
    },
}
SECRET_KEY = 'foobar'
