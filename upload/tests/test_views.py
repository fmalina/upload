from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from upload.models import File, ContentType, get_collection_model
from upload.tests.test_models import create_user

Col = get_collection_model()


def index(request):
    # create dummy account and login the current user
    u = create_user()
    u = authenticate(username=u.username, password='testpw')
    login(request, u)

    user_type = ContentType.objects.get_for_model(u)
    user_img = File.objects.filter(content_type__pk=user_type.id,
                                   object_id=u.id).first()
    return render(request, 'index.html', {
        'img': user_img,
        'list': Col.objects.all()
    })


def album(request, pk):
    col = get_object_or_404(Col, pk=pk)
    return render(request, 'upload/photos/album.html', {
        'photos': col.file_set.all(),
        'col': col
    })
