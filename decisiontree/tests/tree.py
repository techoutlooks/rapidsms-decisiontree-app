from django.conf import settings

from decisiontree import forms
from decisiontree import models
from decisiontree.tests.base import DecisionTreeTestBase


class BasicTreeTest(DecisionTreeTestBase):

    def setUp(self):
        super(BasicTreeTest, self).setUp()
        self.trigger = 'food'
        self.tree = self.create_tree(data={'trigger': self.trigger})
        self.trans = self.create_trans(data={'current_state': self.tree.root_state})

    def test_invalid_trigger(self):
        """Tree app should not respond to an invalid trigger."""
        msg = self._send('i-do-not-exist')
        self.assertTrue(len(msg.responses) == 0)

    def test_valid_trigger(self):
        """Tree app should respond to valid trigger with root state question."""
        msg = self._send(self.trigger)
        question = self.tree.root_state.question.text
        self.assertTrue(question in msg.responses[0].text)

    def test_no_transitions(self):
        """Tree app should end session if no transitions are found."""
        models.Transition.objects.all().delete()
        msg = self._send(self.trigger)
        msg = self._send('can-be-anything')
        session = self.get_session()
        self.assertEqual(session.state, None)
        self.assertEqual(msg.responses[0].text, "No questions found")

    def test_retry(self):
        """Tree app should allow retries if no limit is specified."""
        msg = self._send(self.trigger)
        msg = self._send("i-do-not-exist")
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)
        retry = self.trans.answer.answer
        msg = self._send(retry)
        next_question = self.trans.next_state.question.text
        self.assertTrue(next_question in msg.responses[0].text)

    def test_too_many_retries(self):
        """Tree app should end session if retry limit is hit."""
        self.tree.root_state.num_retries = 2 
        self.tree.root_state.save()
        msg = self._send(self.trigger)
        msg = self._send("i-do-not-exist")
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)
        msg = self._send("i-still-do-not-exist")
        session = self.get_session()
        self.assertEqual(session.state, None)

    def test_basic_response(self):
        """Tree app should send next question after first response."""
        msg = self._send(self.trigger)
        answer = self.trans.answer.answer
        msg = self._send(answer)
        next_question = self.trans.next_state.question.text
        self.assertTrue(next_question in msg.responses[0].text)

    def test_error_response(self):
        """
        If no error response is specified by the question, the tree app should 
        send a error message when there is no transition for the given answer.
        """
        msg = self._send(self.trigger)
        msg = self._send('bad-answer')
        self.assertTrue('is not a valid answer' in msg.responses[0].text)

    def test_error_response_from_question(self):
        """
        If the question specifies an error response, the tree app should send
        this message when there is no transition for the given answer.
        """
        self.tree.root_state.question.error_response = 'my error response'
        self.tree.root_state.question.save()
        msg = self._send(self.trigger)
        msg = self._send('bad-answer')
        self.assertTrue('my error response' == msg.responses[0].text)

    def test_complete_tree(self):
        """
        Tree app should send completion text and end session when there is 
        no state to go to.
        """
        self.tree.completion_text = "done!"
        self.tree.save()
        self.trans.next_state = None
        self.trans.save()
        msg = self._send(self.trigger)
        answer = self.trans.answer.answer
        msg = self._send(answer)
        session = self.get_session()
        self.assertEqual(session.state, None)
        self.assertEqual(msg.responses[0].text, self.tree.completion_text)

    def test_no_completion_text(self):
        """
        Tree app should end session without sending competion text when there
        is no state to go to.
        """
        self.tree.completion_text = None
        self.tree.save()
        self.trans.next_state = None
        self.trans.save()
        msg = self._send(self.trigger)
        answer = self.trans.answer.answer
        msg = self._send(answer)
        session = self.get_session()
        self.assertEqual(session.state, None)
        self.assertEqual(len(msg.responses), 0)

    def test_sequence_start(self):
        msg = self._send(self.trigger)
        answer = self.trans.answer.answer
        msg = self._send(answer)
        entry = self.trans.entries.all()[0]
        self.assertEqual(entry.sequence_id, 1)

    def test_sequence_increment(self):
        trans2 = self.create_trans(data={'current_state': self.trans.next_state})
        self._send(self.trigger)
        msg = self._send(self.trans.answer.answer)
        msg = self._send(trans2.answer.answer)
        entry = trans2.entries.order_by('-sequence_id')[0]
        self.assertEqual(entry.sequence_id, 2)

    def test_sequence_end(self):
        msg = self._send(self.trigger)
        session = self.get_session()
        self.assertNotEqual(session.state, None)
        msg = self._send(settings.DECISIONTREE_SESSION_END_TRIGGER)
        session = self.get_session()
        self.assertEqual(session.state, None)
        self.assertTrue(session.canceled)
        self.assertEqual(msg.responses[0].text, "Your session with '{0}' has ended".format(self.trigger))


class TreesFormTest(DecisionTreeTestBase):

    def setUp(self):
        super(TreesFormTest, self).setUp()
        self.tree_data = {
            'trigger': 'trigger',
            'root_state': self.create_state().pk,
            'completion_text': 'thanks',
            'summary': 'This is a survey.',
        }

    def check_saved_data(self, tree):
        """Checks that the given tree saved as expected from self.tree_data."""    
        self.assertEquals(tree.trigger, self.tree_data['trigger'])
        self.assertEquals(tree.root_state.pk, self.tree_data['root_state'])
        self.assertEquals(tree.completion_text, self.tree_data['completion_text'])
        self.assertEquals(tree.summary, self.tree_data['summary'])

    def test_add_survey(self):
        """The TreesForm should save a complete new Tree object."""
        form = forms.TreesForm(self.tree_data)
        form.save()
        tree = models.Tree.objects.get()
        self.check_saved_data(tree)

    def test_no_keyword(self):
        """The trigger keyword field of the tree should be required."""
        self.tree_data.pop('trigger')
        form = forms.TreesForm(self.tree_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('trigger' in form.errors)

    def test_no_first_state(self):
        """The tree must have a first state."""
        self.tree_data.pop('root_state')
        form = forms.TreesForm(self.tree_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('root_state' in form.errors)

    def test_no_completion_text(self):
        """The completion text field of the tree should be optional."""
        self.tree_data['completion_text'] = ''
        form = forms.TreesForm(self.tree_data)
        form.save()
        tree = models.Tree.objects.get()
        self.check_saved_data(tree)

    def test_no_summary(self):
        """The summary field of the tree should be optional."""
        self.tree_data['summary'] = ''
        form = forms.TreesForm(self.tree_data)
        form.save()
        tree = models.Tree.objects.get()
        self.check_saved_data(tree)
