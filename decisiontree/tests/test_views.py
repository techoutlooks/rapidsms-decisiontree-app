from model_mommy import mommy

from django.core.urlresolvers import reverse

from .. import models
from .cases import DecisionTreeTestCase


class TestSurveySessionClose(DecisionTreeTestCase):
    url_name = 'session_close'

    def setUp(self):
        super(TestSurveySessionClose, self).setUp()

        self.contact = mommy.make('rapidsms.Contact')
        self.contact_link = mommy.make('multitenancy.ContactLink',
                                       contact=self.contact, tenant=self.tenant)
        self.connection = mommy.make('rapidsms.Connection',
                                     contact=self.contact, backend=self.backend,
                                     identity='1112223333')

        self.user = mommy.make('auth.User', is_superuser=True)
        self.make_tenant_manager(self.user)
        self.login_user(self.user)

        self.session = mommy.make('decisiontree.Session',
                                  state=mommy.make('decisiontree.TreeState'),
                                  connection=self.connection)

    def get_url(self, **kwargs):
        kwargs.setdefault('group_slug', self.tenant.group.slug)
        kwargs.setdefault('tenant_slug', self.tenant.slug)
        kwargs.setdefault('pk', self.session.pk)
        return reverse(self.url_name, kwargs=kwargs)

    def test_get(self):
        """Session close view requires POST."""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 405)
        self.session = models.Session.objects.get(pk=self.session.pk)
        self.assertTrue(self.session.is_open())
        self.assertFalse(self.session.is_closed())

    def test_delete(self):
        """Session close view requires POST."""
        response = self.client.delete(self.get_url())
        self.assertEqual(response.status_code, 405)
        self.session = models.Session.objects.get(pk=self.session.pk)
        self.assertTrue(self.session.is_open())
        self.assertFalse(self.session.is_closed())

    def test_non_existant(self):
        """View should return 404 response if session does not exist."""
        response = self.client.post(self.get_url(pk=1234))
        self.assertEqual(response.status_code, 404)
        self.session = models.Session.objects.get(pk=self.session.pk)
        self.assertTrue(self.session.is_open())
        self.assertFalse(self.session.is_closed())

    def test_already_closed(self):
        """Session close view does not act on closed session."""
        # TODO: mock to ensure that save is not called.
        self.session.close()
        response = self.client.post(self.get_url())
        expected_url = reverse('recent_sessions', kwargs={
            'group_slug': self.tenant.group.slug,
            'tenant_slug': self.tenant.slug,
            'pk': self.session.tree.pk,
        })
        self.assertRedirectsNoFollow(response, expected_url)
        self.session = models.Session.objects.get(pk=self.session.pk)
        self.assertTrue(self.session.is_closed())
        self.assertFalse(self.session.is_open())

    def test_close(self):
        """Session close view cancels the session."""
        response = self.client.post(self.get_url())
        expected_url = reverse('recent_sessions', kwargs={
            'group_slug': self.tenant.group.slug,
            'tenant_slug': self.tenant.slug,
            'pk': self.session.tree.pk,
        })
        self.assertRedirectsNoFollow(response, expected_url)
        self.session = models.Session.objects.get(pk=self.session.pk)
        self.assertTrue(self.session.is_closed())
        self.assertFalse(self.session.is_open())
