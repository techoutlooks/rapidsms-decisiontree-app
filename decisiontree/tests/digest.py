from django.core import mail

from decisiontree import models
from decisiontree.tests.base import DecisionTreeTestBase


class DigestTest(DecisionTreeTestBase):
    
    def setUp(self):
        super(DigestTest, self).setUp()
        self.user = self.create_user('test', 'a@a.com', 'abc')
        self.fruit_tag = self.create_tag(data={'name': 'fruit'})
        self.fruit_tag.recipients.add(self.user)
    
    def test_auto_tag_notification(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans1 = self.create_trans(data={'current_state': tree.root_state})
        trans1.tags.add(self.fruit_tag)
        self._send('food')
        msg = self._send(trans1.answer.answer)
        entry = trans1.entries.order_by('-sequence_id')[0]
        self.assertTrue(self.fruit_tag.pk in entry.tags.values_list('pk', flat=True))
        notification = models.TagNotification.objects.all()[0]
        self.assertEqual(notification.entry.pk, entry.pk)

    def test_cron_job(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans1 = self.create_trans(data={'current_state': tree.root_state})
        trans2 = self.create_trans(data={'current_state': trans1.next_state})
        trans1.tags.add(self.fruit_tag)
        self._send('food')
        msg = self._send(trans1.answer.answer)
        msg = self._send(trans2.answer.answer)
        self.app.status_update()
        self.assertEquals(len(mail.outbox), 1)
        notification = models.TagNotification.objects.all()[0]
        self.assertTrue(notification.sent)
