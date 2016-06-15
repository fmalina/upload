from django.conf import settings

# custom model that collects user uploaded albums, file collections
UPLOAD_COLLECTION_MODEL = getattr(settings, 'UPLOAD_COLLECTION_MODEL',
                                            'upload.Collection')
# path where files get uploaded to on the server
UPLOAD_MEDIA_ROOT = getattr(settings, 'UPLOAD_MEDIA_ROOT', settings.MEDIA_ROOT)
# downsize large images to this size
UPLOAD_DOWNSIZE_TO = getattr(settings, 'UPLOAD_DOWNSIZE_TO', (1024, 768))
# fill transparency of uploaded images to this RGB color, white by default
UPLOAD_FILL_ALPHA = getattr(settings, 'UPLOAD_FILL_ALPHA', (255, 255, 255))
