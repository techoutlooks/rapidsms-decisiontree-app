from model_mommy import mommy

from django.conf import settings
from django.core import mail

from rapidsms.messages.incoming import IncomingMessage

from decisiontree.multitenancy import models as link_models
from decisiontree import tasks
from decisiontree import models as dt

from .cases import DecisionTreeTestCase


class BasicSurveyTest(DecisionTreeTestCase):

    def setUp(self):
        super(BasicSurveyTest, self).setUp()
        self.survey = mommy.make('decisiontree.Tree', trigger='food')
        link_models.TreeLink.all_tenants.create(
            linked=self.survey, tenant=self.tenant)
        self.answer = mommy.make('decisiontree.Answer', type='A')
        self.transition = mommy.make(
            'decisiontree.Transition', current_state=self.survey.root_state,
            answer=self.answer, next_state=mommy.make('decisiontree.TreeState'))
        link_models.TransitionLink.all_tenants.create(
            linked=self.transition, tenant=self.tenant)

    def _send(self, text):
        msg = IncomingMessage([self.connection], text)
        self.app.handle(msg)
        return msg

    def test_invalid_trigger(self):
        msg = self._send('i-do-not-exist')
        self.assertTrue(len(msg.responses) == 0)

    def test_valid_trigger(self):
        msg = self._send('food')
        question = self.transition.current_state.question.text
        self.assertTrue(question in msg.responses[0]['text'])

    def test_basic_response(self):
        self._send('food')
        answer = self.transition.answer.answer
        msg = self._send(answer)
        next_question = self.transition.next_state.question.text
        self.assertTrue(next_question in msg.responses[0]['text'])

    def test_error_response(self):
        self._send('food')
        msg = self._send('bad-answer')
        self.assertTrue('is not a valid answer' in msg.responses[0]['text'])

    def test_error_response_from_question(self):
        self.survey.root_state.question.error_response = 'my error response'
        self.survey.root_state.question.save()
        self._send('food')
        msg = self._send('bad-answer')
        self.assertTrue('my error response' == msg.responses[0]['text'])

    def test_sequence_start(self):
        self._send('food')
        answer = self.transition.answer.answer
        self._send(answer)
        entry = self.transition.entries.all()[0]
        self.assertEqual(entry.sequence_id, 1)

    def test_sequence_increment(self):
        answer2 = mommy.make('decisiontree.Answer', type='A')
        transition2 = mommy.make(
            'decisiontree.Transition', current_state=self.transition.next_state,
            answer=answer2)
        link_models.TransitionLink.all_tenants.create(
            linked=transition2, tenant=self.tenant)
        self._send('food')
        self._send(self.transition.answer.answer)
        self._send(transition2.answer.answer)
        entry = transition2.entries.order_by('-sequence_id')[0]
        self.assertEqual(entry.sequence_id, 2)

    def test_sequence_end(self):
        self._send('food')
        session = self.connection.session_set.all()[0]
        self.assertNotEqual(session.state, None)
        msg = self._send('end')
        session = self.connection.session_set.all()[0]
        self.assertEqual(session.state, None)
        self.assertTrue(session.canceled)
        self.assertEqual(msg.responses[0]['text'],
                         "Your session with 'food' has ended")


class DigestTest(DecisionTreeTestCase):

    def setUp(self):
        super(DigestTest, self).setUp()
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, username='test', email='a@a.com')

        self.fruit_tag = mommy.make('decisiontree.Tag', name='fruit')
        self.fruit_tag.recipients.add(self.user)
        link_models.TagLink.all_tenants.create(
            linked=self.fruit_tag, tenant=self.tenant)

        self.survey = mommy.make('decisiontree.Tree', trigger='food')
        link_models.TreeLink.all_tenants.create(
            linked=self.survey, tenant=self.tenant)

    def _send(self, text):
        msg = IncomingMessage([self.connection], text)
        self.app.handle(msg)
        return msg

    def test_auto_tag_notification(self):
        trans1 = mommy.make(
            'decisiontree.Transition', current_state=self.survey.root_state,
            answer=mommy.make('decisiontree.Answer', type='A'),
            next_state=mommy.make('decisiontree.TreeState'))
        trans1.tags.add(self.fruit_tag)
        link_models.TransitionLink.all_tenants.create(
            linked=trans1, tenant=self.tenant)

        self._send('food')
        self._send(trans1.answer.answer)
        entry = trans1.entries.order_by('-sequence_id')[0]
        self.assertTrue(self.fruit_tag.pk in entry.tags.values_list('pk', flat=True))
        notification = dt.TagNotification.objects.all()[0]
        self.assertEqual(notification.entry.pk, entry.pk)

    def test_task(self):  # TODO: move to separate module
        trans1 = mommy.make(
            'decisiontree.Transition', current_state=self.survey.root_state,
            answer=mommy.make('decisiontree.Answer', type='A'),
            next_state=mommy.make('decisiontree.TreeState'))
        trans1.tags.add(self.fruit_tag)
        link_models.TransitionLink.all_tenants.create(
            linked=trans1, tenant=self.tenant)

        trans2 = mommy.make(
            'decisiontree.Transition', current_state=trans1.next_state,
            next_state=mommy.make('decisiontree.TreeState'))
        link_models.TransitionLink.all_tenants.create(
            linked=trans2, tenant=self.tenant)

        self._send('food')
        self._send(trans1.answer.answer)
        self._send(trans2.answer.answer)
        tasks.status_update()
        self.assertEquals(len(mail.outbox), 1)
        notification = dt.TagNotification.objects.all()[0]
        self.assertTrue(notification.sent)
