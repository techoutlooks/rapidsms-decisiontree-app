from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from decisiontree.models import (
    Answer, Entry, Question, Tag, TagNotification, Transition, Tree, TreeState)
from decisiontree.utils import parse_tags, edit_string_for_tags


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['name', 'type', 'answer', 'description']


class TreesForm(forms.ModelForm):

    class Meta:
        model = Tree
        fields = ['trigger', 'root_state', 'completion_text', 'summary']

    def __init__(self, *args, **kwargs):
        super(TreesForm, self).__init__(*args, **kwargs)
        states = TreeState.objects.select_related('question')
        states = states.order_by('question__text')
        self.fields['root_state'].label = 'First State'
        self.fields['root_state'].queryset = states
        self.fields['trigger'].label = 'Keyword'


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text', 'error_response']


class StateForm(forms.ModelForm):

    class Meta:
        model = TreeState
        fields = ['name', 'question', 'num_retries']


class ReportForm(forms.Form):
    ANALYSIS_TYPES = (
        ('A', 'Mean'),
        ('R', 'Median'),
        ('C', 'Mode'),
    )
    # answer = forms.CharField(label=("answer"),required=False)
    dataanalysis = forms.ChoiceField(choices=ANALYSIS_TYPES)


class AnswerSearchForm(forms.Form):
    # ANALYSIS_TYPES = (
    #     ('A', 'Mean'),
    #     ('R', 'Median'),
    #     ('C', 'Mode'),
    # )
    # answer = forms.ModelChoiceField(queryset=Answer.objects.none())
    # analysis = forms.ChoiceField(choices=ANALYSIS_TYPES)
    tag = forms.ModelChoiceField(queryset=Tag.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree')
        super(AnswerSearchForm, self).__init__(*args, **kwargs)
        # answers = \
        #     Answer.objects.filter(transitions__entries__session__tree=tree)
        tags = Tag.objects.filter(entries__session__tree=tree).distinct()

        # self.fields['answer'].queryset = answers.distinct()
        self.fields['tag'].queryset = tags
        # self.fields['analysis'].label = 'Calculator'
        # self.fields['tag'].label = 'Calculator'


class TagWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags(Tag.objects.filter(id__in=value))
        return super(TagWidget, self).render(name, value, attrs)


class TagField(forms.CharField):
    widget = TagWidget

    def __init__(self, *args, **kwargs):
        if 'help_text' not in kwargs:
            kwargs['help_text'] = ('Tags with spaces must be quoted, for '
                                   'example: apple "ball cat" dog, will '
                                   'result in "apple", "ball cat", and "dog" tags')
        super(TagField, self).__init__(*args, **kwargs)

    def clean(self, value):
        try:
            tag_names = parse_tags(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        return tags


class EntryTagForm(forms.ModelForm):
    tags = TagField()

    class Meta:
        model = Entry
        fields = ['tags']

    def save(self):
        entry = super(EntryTagForm, self).save()
        # create tag notifications
        TagNotification.create_from_entry(entry)
        return entry


class PathForm(forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = Transition
        fields = ['current_state', 'answer', 'next_state', 'tags']

    def __init__(self, *args, **kwargs):
        super(PathForm, self).__init__(*args, **kwargs)
        states = TreeState.objects.select_related('question')
        states = states.order_by('question__text')
        self.fields['current_state'].queryset = states
        self.fields['current_state'].label = 'Current State'
        self.fields['answer'].label = 'Answer'
        self.fields['answer'].queryset = Answer.objects.order_by('answer')
        self.fields['next_state'].label = 'Next State'
        self.fields['next_state'].queryset = states
        self.fields['tags'].label = 'Auto tags'


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name', 'recipients']

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['recipients'] = forms.ModelMultipleChoiceField(
            required=False, widget=forms.CheckboxSelectMultiple,
            queryset=get_user_model().objects.exclude(email=''))


class TreeSummaryForm(forms.ModelForm):

    class Meta:
        model = Tree
        fields = ['summary']

    def __init__(self, *args, **kwargs):
        super(TreeSummaryForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget = forms.Textarea()
