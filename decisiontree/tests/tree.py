from decisiontree import forms
from decisiontree import models
from decisiontree.tests.base import DecisionTreeTestBase


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
        """
        Checks that the given tree saved as expected from self.tree_data.
        """
        self.assertEqual(tree.trigger, self.tree_data['trigger'])
        self.assertEqual(tree.root_state.pk, self.tree_data['root_state'])
        self.assertEqual(tree.completion_text, 
                self.tree_data['completion_text'])
        self.assertEqual(tree.summary, self.tree_data['summary'])

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
