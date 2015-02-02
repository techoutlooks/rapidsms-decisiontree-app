import mock

from django.test import TestCase

from ..templatetags import tree_tags


@mock.patch('decisiontree.multitenancy.utils.multitenancy_enabled')
@mock.patch('decisiontree.templatetags.tree_tags.reverse')
class TestTenancyUrl(TestCase):

    def setUp(self):
        super(TestTenancyUrl, self).setUp()
        self.request = mock.Mock(group_slug='group', tenant_slug='tenant')
        self.context = {'request': self.request}

    def test_tenancy_enabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = True
        val = tree_tags.tenancy_url(self.context, 'test_url', 'a', b='b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': ('a',),
            'kwargs': {
                'tenant_slug': self.request.tenant_slug,
                'group_slug': self.request.group_slug,
                'b': 'b',
            },
        })

    def test_tenancy_disabled(self, reverse, multitenancy_enabled):
        multitenancy_enabled.return_value = False
        val = tree_tags.tenancy_url(self.context, 'test_url', 'a', b='b')
        self.assertTrue(isinstance(val, mock.Mock))
        self.assertTrue(reverse.call_count, 1)
        self.assertEqual(reverse.call_args[0], ('test_url',))
        self.assertEqual(reverse.call_args[1], {
            'args': ('a',),
            'kwargs': {
                'b': 'b',
            },
        })
