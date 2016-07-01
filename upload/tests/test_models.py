from django.test import TestCase
from django.contrib.auth.models import User
from upload.models import File
from upload.models import get_collection_model

Col = get_collection_model()

class FileTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user('Bob', 'bob@example.com', 'testpw')
        u.save()
        c = Col.objects.create(user=u)
        f = File(alt='Bob', col=c)
        f.save()

    def test_model(self):
        f = File.objects.first()
        self.assertEqual(f.pk, 1)
        self.assertEqual(f.alt, 'Bob')
        #print(f.path())
        #self.assertTrue(f.path().endswith('upload/static/media/0/1/1.jpg'))