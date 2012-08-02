from decisiontree import conf
from decisiontree import models
from decisiontree.tests.base import DecisionTreeTestBase


class AppTest(DecisionTreeTestBase):
    """Tests of the functionality in decisiontree.apps"""

    def setUp(self):
        super(AppTest, self).setUp()
        self.trigger = 'food'
        root_question = self.create_question(data={'text': 'root'})
        root_state = self.create_state(data={'question': root_question})
        next_question = self.create_question(data={'text': 'next'})
        next_state = self.create_state(data={'question': next_question})
        self.tree = self.create_tree(
            data={'trigger': self.trigger, 'root_state': root_state})
        self.trans = self.create_trans(
            data={'current_state': root_state, 'next_state': next_state})

    def test_invalid_trigger(self):
        """Tree app should not respond to an invalid trigger."""
        msg = self._send('i-do-not-exist')
        self.assertTrue(len(msg.responses) == 0)

    def test_valid_trigger(self):
        """
        Tree app should respond to valid trigger with root state question.
        """
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
        trans2 = self.create_trans(
                data={'current_state': self.trans.next_state})
        self._send(self.trigger)
        msg = self._send(self.trans.answer.answer)
        msg = self._send(trans2.answer.answer)
        entry = trans2.entries.order_by('-sequence_id')[0]
        self.assertEqual(entry.sequence_id, 2)

    def test_sequence_end(self):
        msg = self._send(self.trigger)
        session = self.get_session()
        self.assertNotEqual(session.state, None)
        msg = self._send(conf.SESSION_END_TRIGGER)
        session = self.get_session()
        self.assertEqual(session.state, None)
        self.assertTrue(session.canceled)
        self.assertEqual(msg.responses[0].text, 
                "Your session with '{0}' has ended".format(self.trigger))

    def test_exact_match(self):
        """Tree app should move to next state if exact answer matches."""
        self.trans.answer.answer = 'exact'
        self.trans.answer.type = 'A'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('exact')
        session = self.get_session()
        self.assertEqual(session.state, self.trans.next_state)

    def test_exact_no_match(self):
        """
        Tree app should not move to next state if exact answer doesn't match.
        """
        self.trans.answer.answer = 'exact'
        self.trans.answer.type = 'A'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('this-will-not-match')
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)

    def test_exact_no_match_blank(self):
        """Tree app should not respond to a blank message."""
        msg = self._send(self.trigger)
        msg = self._send('')
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)

    def test_exact_match_case_insensitive(self):
        """Answer matches should be case insensitive."""
        self.trans.answer.answer = 'exact'
        self.trans.answer.type = 'A'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('ExAcT')
        session = self.get_session()
        self.assertEqual(session.state, self.trans.next_state)

    def test_regex_match(self):
        """Tree app should move to next state if the regex answer matches."""
        self.trans.answer.answer = '^[a-z]+$'
        self.trans.answer.type = 'R'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('lettersonly')
        session = self.get_session()
        self.assertEqual(session.state, self.trans.next_state)

    def test_regex_no_match(self):
        """
        Tree app should not move to next state if regex answer doesn't match.
        """
        self.trans.answer.answer = '^[a-z]+$'
        self.trans.answer.type = 'R'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('Th1$ 1$ @ b@d m3$$3g3')
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)

    def test_regex_match_case_insensitive(self):
        """Answer matches should be case insensitive."""
        self.trans.answer.answer = '^[a-z]+$'
        self.trans.answer.type = 'R'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        msg = self._send('AFancyMessage')
        session = self.get_session()
        self.assertEqual(session.state, self.trans.next_state)

    def test_custom_logic_match(self):
        """Tree app should be able to use custom logic to validate answers."""
        self.trans.answer.answer = 'testfunc'
        self.trans.answer.type = 'C'
        self.trans.answer.save()
        test_func = lambda m: m.text == 'abc123'
        self.app.register_custom_transition('testfunc', test_func)
        msg = self._send(self.trigger)
        msg = self._send('abc123')
        session = self.get_session()
        self.assertEqual(session.state, self.trans.next_state)

    def test_custom_logic_no_match(self):
        """Tree app should be able to use custom logic to validate answers."""
        self.trans.answer.answer = 'testfunc'
        self.trans.answer.type = 'C'
        self.trans.answer.save()
        test_func = lambda m: m.text == 'abc123'
        self.app.register_custom_transition('testfunc', test_func)
        msg = self._send(self.trigger)
        msg = self._send('not-going-to-work')
        session = self.get_session()
        self.assertEqual(session.state, self.tree.root_state)

    def test_custom_logic_unregistered_function(self):
        """If no function is registered, an Exception should be thrown."""
        self.trans.answer.answer = 'nonexistantfunc'
        self.trans.answer.type = 'C'
        self.trans.answer.save()
        msg = self._send(self.trigger)
        self.assertRaises(Exception, self._send, ['not-going-to-work'])

    def test_add_session_listener(self):
        """
        Session listener functions should execute at the beginning and end
        of every session.
        """
        def listener(session, is_ending):
            # A simple way to check that listeners are being executed at the 
            # beginning and end of each session.
            if not is_ending:
                session.tree.root_state.question.text = 'started'
                session.tree.root_state.question.save()
            else:
                session.tree.completion_text = 'ending'
                session.tree.save()

        try:
            self.app.set_session_listener(self.trigger, listener)
            msg = self._send(self.trigger)
            self.assertTrue(msg.responses[0], 'started')
            msg = self._send(conf.SESSION_END_TRIGGER)
            self.assertTrue(msg.responses[0], 'ending')

        # Clean up since the test runner likes to leave this around.
        finally:
            self.app.session_listeners.pop(self.trigger)

    def test_multiple_sessions(self):
        """Only one session should occur at a time."""
        tree2 = self.create_tree(data={'trigger': 'troll'})

        msg = self._send(self.trigger)
        first_session_id = self.get_session().id
        initial_response = self.tree.root_state.question.text
        self.assertEqual(msg.responses[0].text, initial_response)
        
        msg = self._send('troll')
        second_session_id = self.get_session().id
        self.assertTrue('is not a valid answer' in msg.responses[0].text)

        self.assertEqual(first_session_id, second_session_id)

    def test_multiple_connections(self):
        """Multiple connections should be handled separately."""
        msg1 = self._send(self.trigger, self.connection)
        msg2 = self._send(self.trigger, self.connection2)
        initial_response = self.tree.root_state.question.text
        for msg in (msg1, msg2):
            self.assertEqual(msg.responses[0].text, initial_response)

        answer = self.trans.answer.answer
        msg1 = self._send(answer, self.connection)
        msg2 = self._send(answer, self.connection2)
        response = self.trans.next_state.question.text
        for msg in (msg1, msg2):
            self.assertEqual(msg.responses[0].text, response)
