from django.conf import settings

# root path where files get uploaded on the server
UPLOAD_ROOT = getattr(settings, 'UPLOAD_ROOT', settings.MEDIA_ROOT)

# downsize large images to this size
UPLOAD_DOWNSIZE_TO = getattr(settings, 'UPLOAD_DOWNSIZE_TO', (1024, 768))
# minimum acceptable image width and height
UPLOAD_MIN_SIZE = getattr(settings, 'UPLOAD_MIN_SIZE', 200)
# fill transparency of uploaded images to this RGB color, white by default
UPLOAD_FILL_ALPHA = getattr(settings, 'UPLOAD_FILL_ALPHA', (255, 255, 255))
# email upload features
UPLOAD_IMAP_ENABLED = getattr(settings, 'UPLOAD_IMAP_ENABLED', False)
UPLOAD_IMAP_EMAIL = getattr(settings, 'UPLOAD_IMAP_EMAIL', 'upload@example.com')
UPLOAD_THUMB_SIZES = getattr(settings, 'UPLOAD_THUMB_SIZES', {
    "tiny": "50x50",
    "small": "100x100",
    "medium": "200x200",
    "large": "400x400",
})
