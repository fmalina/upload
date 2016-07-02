from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from upload.models import get_collection_model
from upload.tests.test_models import create_user

Col = get_collection_model()


def index(request):
    # create dummy account and login the current user
    u = create_user()
    u = authenticate(username=u.username, password='testpw')
    login(request, u)
    return render(request, 'index.html', {
        'list': Col.objects.all()
    })


def album(request, pk):
    alb = get_object_or_404(Col, pk=pk)
    return render(request, 'album.html', {
        'album': alb
    })
