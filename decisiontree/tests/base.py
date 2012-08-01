import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from rapidsms.messages.incoming import IncomingMessage
from rapidsms.models import Connection, Contact, Backend
from rapidsms.tests.harness import MockRouter

from decisiontree import models as dt
from decisiontree.app import App as DecisionApp


class DecisionTreeTestBase(TestCase):
    """A collection of helper methods common to most DecisionTree tests."""

    def setUp(self):
        self.backend = Backend.objects.create(name='test-backend')
        self.router = MockRouter()
        self.app = DecisionApp(router=self.router)

        # Default used by self._send and self.get_session.
        self.contact = Contact.objects.create(name='John Doe')
        self.connection = Connection.objects.create(contact=self.contact,
                backend=self.backend, identity='1112223333')

        # Occasionally used by some tests; not a default.
        self.contact2 = Contact.objects.create(name='Jane Doe')
        self.connection2 = Connection.objects.create(contact=self.contact2,
                backend=self.backend, identity='5558675309')

    def _send(self, text, connection=None):
        """Creates a message using text and handles it using self.app.
        
        Returns the message that is sent.
        """
        connection = connection or self.connection
        msg = IncomingMessage(connection, text)
        self.app.handle(msg)
        return msg

    def get_session(self, connection=None):
        connection = connection or self.connection
        return connection.session_set.all()[0]

    def random_string(self, length=255, extra_chars=''):
        chars = string.letters + extra_chars
        return ''.join([random.choice(chars) for i in range(length)])

    def create_user(self, username=None, email=None, password=None):
        username = username or self.random_string(25)
        email = email or self.random_string(10) + "@test.com"
        password = password or self.random_string(25)
        return User.objects.create_user(username, email, password)

    def create_tree(self, data={}):
        defaults = {
            'trigger': self.random_string(5),
        }
        defaults.update(data)
        if 'root_state' not in data:
            defaults['root_state'] = self.create_state()
        return dt.Tree.objects.create(**defaults)

    def create_state(self, data={}):
        defaults = {
            'name': self.random_string(10),
        }
        defaults.update(data)
        if 'question' not in defaults:
            defaults['question'] = self.create_question()
        return dt.TreeState.objects.create(**defaults)

    def create_question(self, data={}):
        defaults = {
            'text': self.random_string(15),
        }
        defaults.update(data)
        return dt.Question.objects.create(**defaults)
    
    def create_trans(self, data={}):
        defaults = {}
        defaults.update(data)
        if 'current_state' not in defaults:
            defaults['current_state'] = self.create_state()
        if 'answer' not in defaults:
            defaults['answer'] = self.create_answer()
        if 'next_state' not in defaults:
            defaults['next_state'] = self.create_state()
        return dt.Transition.objects.create(**defaults)

    def create_answer(self, data={}):
        defaults = {
            'name': self.random_string(15),
            'type': 'A',
            'answer': self.random_string(5),
        }
        defaults.update(data)
        return dt.Answer.objects.create(**defaults)
    
    def create_tag(self, data={}):
        defaults = {
            'name': self.random_string(15),
        }
        defaults.update(data)
        return dt.Tag.objects.create(**defaults)
