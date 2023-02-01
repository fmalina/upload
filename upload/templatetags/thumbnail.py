from django import template
from django.conf import settings
from upload import app_settings
import subprocess
import os

register = template.Library()


@register.simple_tag
def thumbnail(path, size_name='medium', crop='center'):
    if not path:
        return
    size = app_settings.UPLOAD_THUMB_SIZES[size_name]
    new_path = path.replace('.', f'-thumb-{size_name}-{crop}.')
    if not os.path.exists(new_path):
        # smart cropping
        if crop == 'smart':
            trim_arg = "-trim"
            gravity_arg = ''
            extent_arg = ''
        else:
            if crop == '':
                crop = 'center'
            trim_arg = ''
            gravity_arg = f"-gravity {crop}"
            extent_arg = f"-extent {size}"
        output_arg = f"-thumbnail {size}^ {gravity_arg} {extent_arg} {trim_arg}"

        cmd = f"convert {path} {output_arg} {new_path}"
        subprocess.run(cmd, shell=True)
    # path to URL
    url = new_path.replace(settings.STATIC_ROOT, '/')
    return url
