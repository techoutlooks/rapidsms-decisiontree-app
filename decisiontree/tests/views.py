from django.core.urlresolvers import reverse

from decisiontree import models as dt
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
        

class TreeCRUDTestCase(DecisionTreeTestBase):
    "Create/update/delete trees."

    def setUp(self):
        self.user = self.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

    def test_render_create_page(self):
        "Render the create tree form without errors."
        url = reverse('add_tree')
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

    def test_create_tree(self):
        "Submit data to create a new tree."
        data = {
            'root_state': self.create_state().pk,
            'trigger': 'test',
        }
        url = reverse('add_tree')
        response = self.client.post(url, data=data)
        self.assertRedirects(response, reverse('list-surveys'))
        self.assertEqual(dt.Tree.objects.filter(trigger='test').count(), 1)

    def test_render_edit_page(self):
        "Render the edit tree form without errors."
        tree = self.create_tree()
        url = reverse('insert_tree', args=(tree.pk, ))
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

    def test_edit_tree(self):
        "Submit data to edit an existing tree."
        tree = self.create_tree()
        data = {
            'root_state': tree.root_state_id,
            'trigger': 'test',
        }
        url = reverse('insert_tree', args=(tree.pk, ))
        response = self.client.post(url, data=data)
        self.assertRedirects(response, reverse('list-surveys'))
        self.assertEqual(dt.Tree.objects.filter(trigger='test').count(), 1)

    def test_delete_tree(self):
        "Delete a tree."
        tree = self.create_tree()
        url = reverse('delete_tree', args=(tree.pk, ))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('list-surveys'))
        self.assertEqual(dt.Tree.objects.filter(pk=tree.pk).count(), 0)

    def test_delete_requires_post(self):
        "Deleting a tree should require post."
        tree = self.create_tree()
        url = reverse('delete_tree', args=(tree.pk, ))
        response = self.client.get(url)
        self.assertTrue(response.status_code, 405)
