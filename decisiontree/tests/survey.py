from decisiontree.tests.base import DecisionTreeTestBase


class BasicSurveyTest(DecisionTreeTestBase):

    def setUp(self):
        super(BasicSurveyTest, self).setUp()

    def test_invalid_trigger(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        msg = self._send('i-do-not-exist')
        self.assertTrue(len(msg.responses) == 0)

    def test_valid_trigger(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        msg = self._send('food')
        question = trans.current_state.question.text
        self.assertTrue(question in msg.responses[0].text)

    def test_basic_response(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        self._send('food')
        answer = trans.answer.answer
        msg = self._send(answer)
        next_question = trans.next_state.question.text
        self.assertTrue(next_question in msg.responses[0].text)

    def test_error_response(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        self._send('food')
        msg = self._send('bad-answer')
        self.assertTrue('is not a valid answer' in msg.responses[0].text)

    def test_error_response_from_question(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        tree.root_state.question.error_response = 'my error response'
        tree.root_state.question.save()
        self._send('food')
        msg = self._send('bad-answer')
        self.assertTrue('my error response' == msg.responses[0].text)

    def test_sequence_start(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans = self.create_trans(data={'current_state': tree.root_state})
        self._send('food')
        answer = trans.answer.answer
        msg = self._send(answer)
        entry = trans.entries.all()[0]
        self.assertEqual(entry.sequence_id, 1)

    def test_sequence_increment(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans1 = self.create_trans(data={'current_state': tree.root_state})
        trans2 = self.create_trans(data={'current_state': trans1.next_state})
        self._send('food')
        msg = self._send(trans1.answer.answer)
        msg = self._send(trans2.answer.answer)
        entry = trans2.entries.order_by('-sequence_id')[0]
        self.assertEqual(entry.sequence_id, 2)

    def test_sequence_end(self):
        tree = self.create_tree(data={'trigger': 'food'})
        trans1 = self.create_trans(data={'current_state': tree.root_state})
        self._send('food')
        session = self.connection.session_set.all()[0]
        self.assertNotEqual(session.state, None)
        msg = self._send('end')
        session = self.connection.session_set.all()[0]
        self.assertEqual(session.state, None)
        self.assertTrue(session.canceled)
        self.assertEqual(msg.responses[0].text,
                         "Your session with 'food' has ended")
