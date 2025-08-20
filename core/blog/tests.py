from django.test import TestCase
from django.urls import reverse, resolve
from .views import PostViewset


class TestUrl(TestCase):

    def test_blog_index_url_resolve(self):
        url = reverse('blog:index')
        self.assertEqual(resolve(url).func)

