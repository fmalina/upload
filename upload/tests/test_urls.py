from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from upload.tests.test_views import index, album

urlpatterns = [
    path('', index),
    path('<int:pk>', album),
    path('upload/', include('upload.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
