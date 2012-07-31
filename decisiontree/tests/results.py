from rapidsms.messages.incoming import IncomingMessage

from decisiontree.handlers.results import ResultsHandler
from decisiontree.tests.base import DecisionTreeTestBase


class ResultsTest(DecisionTreeTestBase):

    def setUp(self):
        super(ResultsTest, self).setUp()
        text = 'Do you like apples or squash more?'
        self.q = self.create_question(data={'text': text})
        self.fruit = self.create_answer(data={'name': 'apples', 'answer': 'apples'})
        self.state = self.create_state(data={'name': 'food', 'question': self.q})
        self.tree = self.create_tree(data={'trigger': 'food', 'root_state': self.state})

    def _send(self, text):
        """Overrides super."""
        msg = IncomingMessage(self.connection, text)
        handler = ResultsHandler(self.router, msg)
        handler.handle(msg.text)
        return handler

    def test_survey_does_not_exist(self):
        handler = self._send('i-do-not-exist')
        response = handler.msg.responses[0].text
        self.assertEqual(response, 'Survey "i-do-not-exist" does not exist')

    def test_empty_summary(self):
        handler = self._send('food')
        response = handler.msg.responses[0].text
        self.assertEqual(response, 'No summary for "food" survey')

    def test_summary_response(self):
        self.tree.summary = '10 people like food'
        self.tree.save()
        handler = self._send('food')
        response = handler.msg.responses[0].text
        self.assertEqual(response, '10 people like food')

    def test_percent_in_summary(self):
        self.tree.summary = 'we are 100%'
        self.tree.save()
        handler = self._send('food')
        response = handler.msg.responses[0].text
        self.assertEqual(response, 'we are 100%')
