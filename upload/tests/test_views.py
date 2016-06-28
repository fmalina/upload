from django.shortcuts import get_object_or_404, render, redirect
from upload.models import get_collection_model

Col = get_collection_model()


def index(request):
    return render(request, 'index.html', {
        'list': Col.objects.all()
    })


def album(request, pk):
    alb = get_object_or_404(Col, pk=pk)
    return render(request, 'album.html', {
        'album': alb
    })
