import mock

from django.test import TestCase

from .. import utils


@mock.patch('decisiontree.multitenancy.utils.multitenancy_enabled')
@mock.patch('decisiontree.multitenancy.utils.reverse')
class TestTenancyReverse(TestCase):

    def setUp(self):
        super(TestTenancyReverse, self).setUp()
        self.request = mock.Mock(group_slug='group', tenant_slug='tenant')

    def test_args_tenancy_enabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = True
        val = utils.tenancy_reverse(self.request, 'test_url', 'a', 'b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': (self.request.group_slug, self.request.tenant_slug, 'a', 'b'),
            'kwargs': {},
        })

    def test_args_tenancy_disabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = False
        val = utils.tenancy_reverse(self.request, 'test_url', 'a', 'b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': ('a', 'b'),
            'kwargs': {},
        })

    def test_kwargs_tenancy_enabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = True
        val = utils.tenancy_reverse(self.request, 'test_url', a='a', b='b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': (),
            'kwargs': {
                'tenant_slug': self.request.tenant_slug,
                'group_slug': self.request.group_slug,
                'a': 'a',
                'b': 'b',
            },
        })

    def test_kwargs_tenancy_disabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = False
        val = utils.tenancy_reverse(self.request, 'test_url', a='a', b='b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': (),
            'kwargs': {
                'a': 'a',
                'b': 'b',
            },
        })
