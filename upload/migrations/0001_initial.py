# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
from django.db.models import deletion
from upload import app_settings

CUSTOM_COLLECTION = app_settings.UPLOAD_COLLECTION_MODEL != 'upload.Collection'

initial_operations = []

if True: #  if not CUSTOM_COLLECTION? (DB table is still needed for tests)
    initial_operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                            serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=deletion.CASCADE,
                            to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    if CUSTOM_COLLECTION:
        app_name = app_settings.UPLOAD_COLLECTION_MODEL.split('.')[0]
        dependencies += [(app_name, '__first__')]

    operations = initial_operations + [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                            serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(blank=True, editable=False,
                            null=True, verbose_name='legacy #')),
                ('pos', models.IntegerField(blank=True, null=True,
                            verbose_name='order position')),
                ('alt', models.CharField(blank=True, max_length=60)),
                ('fn', models.CharField(blank=True, editable=False,
                            max_length=60, verbose_name='original filename')),
                ('col', models.ForeignKey(blank=True, null=True,
                            on_delete=deletion.CASCADE,
                            to=app_settings.UPLOAD_COLLECTION_MODEL)),
            ],
            options={
                'ordering': ['col', 'pos'],
            },
        ),
    ]
