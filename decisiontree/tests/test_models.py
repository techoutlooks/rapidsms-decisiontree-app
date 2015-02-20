from model_mommy import mommy

from django.test import TestCase

from decisiontree import models


class TestSessionModel(TestCase):

    def setUp(self):
        super(TestSessionModel, self).setUp()
        self.tenant = mommy.make('multitenancy.Tenant')

        self.backend = mommy.make('rapidsms.Backend')
        mommy.make(
            'multitenancy.BackendLink', backend=self.backend, tenant=self.tenant)

        self.contact = mommy.make('rapidsms.Contact')
        mommy.make(
            'multitenancy.ContactLink', contact=self.contact, tenant=self.tenant)

        self.connection = mommy.make(
            'rapidsms.Connection', backend=self.backend, contact=self.contact)

        self.session = mommy.make('decisiontree.Session', connection=self.connection)

    def test_open(self):
        """is_open() is True if session has a state and is not canceled."""
        self.session.canceled = False
        self.session.state = mommy.make('decisiontree.TreeState')
        self.session.save()
        self.assertTrue(self.session.is_open())
        self.assertFalse(self.session.is_closed())

    def test_closed_no_state(self):
        """is_closed() is True if session has no state."""
        self.session.canceled = False
        self.session.state = None
        self.session.save()
        self.assertTrue(self.session.is_closed())
        self.assertFalse(self.session.is_open())

    def test_closed_canceled(self):
        """is_closed() is True if session is canceled."""
        self.session.canceled = True
        self.session.state = mommy.make('decisiontree.TreeState')
        self.session.save()
        self.assertTrue(self.session.is_closed())
        self.assertFalse(self.session.is_open())

    def test_closed_no_state_and_canceled(self):
        """is_closed() is True if session has no state and is canceled."""
        self.session.canceled = True
        self.session.state = None
        self.session.save()
        self.assertTrue(self.session.is_closed())
        self.assertFalse(self.session.is_open())

    def test_manager_open(self):
        """Session is in open() queryset if it has a state and is not canceled."""
        self.session.canceled = False
        self.session.state = mommy.make('decisiontree.TreeState')
        self.session.save()

        open_qs = models.Session.objects.open()
        self.assertEqual(len(open_qs), 1)
        self.assertTrue(self.session in open_qs)

        closed_qs = models.Session.objects.closed()
        self.assertEqual(len(closed_qs), 0)

    def test_manager_closed_no_state(self):
        """Session is in closed() queryset if it has no state."""
        self.session.canceled = False
        self.session.state = None
        self.session.save()

        open_qs = models.Session.objects.open()
        self.assertEqual(len(open_qs), 0)

        closed_qs = models.Session.objects.closed()
        self.assertEqual(len(closed_qs), 1)
        self.assertTrue(self.session in closed_qs)

    def test_manager_closed_canceled(self):
        """Session is in closed() queryset if it is canceled."""
        self.session.canceled = True
        self.session.state = mommy.make('decisiontree.TreeState')
        self.session.save()

        open_qs = models.Session.objects.open()
        self.assertEqual(len(open_qs), 0)

        closed_qs = models.Session.objects.closed()
        self.assertEqual(len(closed_qs), 1)
        self.assertTrue(self.session in closed_qs)

    def test_manager_closed_no_state_and_canceled(self):
        """Session is in closed() queryset if it has no state and is canceled."""
        self.session.canceled = True
        self.session.state = None
        self.session.save()

        open_qs = models.Session.objects.open()
        self.assertEqual(len(open_qs), 0)

        closed_qs = models.Session.objects.closed()
        self.assertEqual(len(closed_qs), 1)
        self.assertTrue(self.session in closed_qs)
