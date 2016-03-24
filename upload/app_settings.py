from django.conf import settings

UPLOAD = getattr(settings, 'UPLOAD', {
    'collection_model': 'upload.Collection',
    'media_root': settings.MEDIA_ROOT,
    'downsize_to': (1024, 768),
    'fill_transparent': (255, 255, 255), # Use False to keep PNG aplha
})
