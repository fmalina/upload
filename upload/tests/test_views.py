from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from upload.models import File, Collection, ContentType
from upload.tests.test_models import create_user


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
        'list': Collection.objects.all()
    })


def album(request, pk):
    obj = get_object_or_404(Collection, pk=pk)
    return render(request, 'upload/photos/album.html', {
        'photos': obj.file_set.all(),
        'obj': obj,
        'size': '180x180'
    })
