DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
PROJECT_ROOT = '/Users/f/Desktop/upload/'
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'uploads',
        'USER': 'root',
        'PASSWORD': ''
    }
}

MEDIA_ROOT = PROJECT_ROOT + 'm/'
MEDIA_URL = '/m/'
SECRET_KEY = '-'
TEMPLATE_DIRS = (PROJECT_ROOT + 'apps/templates/',)
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.ServerError'
)
ROOT_URLCONF = 'urls'
INSTALLED_APPS = (
    'upload',
)