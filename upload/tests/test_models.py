from django.test import TestCase
from django.contrib.auth.models import User
from upload.models import File, get_collection_model

Col = get_collection_model()


def create_user():
    u = User.objects.first()
    if not u:
        u = User.objects.create_user('Frank', 'f@example.com', 'testpw')
        u.save()
    return u


class FileTestCase(TestCase):
    def setUp(self):
        u = create_user()
        c = Col.objects.create(user=u)
        f = File(alt='Frank', col=c)
        f.save()

    def test_model(self):
        f = File.objects.first()
        self.assertEqual(f.pk, 1)
        self.assertEqual(f.alt, 'Frank')
        self.assertTrue(f.path().endswith('upload/static/media/0/1/1.jpg'))
