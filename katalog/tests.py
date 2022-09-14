from django.test import TestCase, Client
from django.urls import resolve
from .views import show_katalog

# Create your tests here.
class KatalogAppTest(TestCase):
    def test_katalog_app_url_routed_and_responds(self):
        response = Client().get('/katalog/')
        self.assertEqual(response.status_code,200)

    def test_katalog_app_using_katalog_template(self):
        response = Client().get('/katalog/')
        self.assertTemplateUsed(response, 'katalog.html')