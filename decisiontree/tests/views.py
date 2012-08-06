from django.core.urlresolvers import reverse

from decisiontree.tests.base import DecisionTreeTestBase


class IndexViewTestCase(DecisionTreeTestBase):
    "Simple entry point page."

    def setUp(self):
        self.user = self.create_user(username='test', password='test')
        self.client.login(username='test', password='test')
        self.url = reverse('list-surveys')

    def test_get_page(self):
        "Fetch the page without errors."
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)       
        
