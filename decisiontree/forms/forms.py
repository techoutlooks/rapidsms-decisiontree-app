from django import forms
from django.contrib.auth import get_user_model

from decisiontree.multitenancy.forms import TenancyModelForm

from .. import models
from .fields import TagField


class AnswerCreateUpdateForm(TenancyModelForm):

    class Meta:
        model = models.Answer
        fields = ['name', 'type', 'answer', 'description']


class AnswerSearchForm(forms.Form):
    # ANALYSIS_TYPES = (
    #     ('A', 'Mean'),
    #     ('R', 'Median'),
    #     ('C', 'Mode'),
    # )
    # answer = forms.ModelChoiceField(queryset=models.Answer.objects.none())
    # analysis = forms.ChoiceField(choices=ANALYSIS_TYPES)
    tag = forms.ModelChoiceField(
        required=False, empty_label="All Tags",
        queryset=models.Tag.objects.none())

    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree')
        super(AnswerSearchForm, self).__init__(*args, **kwargs)
        # answers = models.Answer.objects.filter(transitions__entries__session__tree=tree)
        tags = models.Tag.objects.filter(entries__session__tree=tree).distinct()

        # self.fields['answer'].queryset = answers.distinct()
        self.fields['tag'].queryset = tags
        # self.fields['analysis'].label = 'Calculator'
        # self.fields['tag'].label = 'Calculator'


class EntryTagForm(TenancyModelForm):
    tags = TagField()

    class Meta:
        model = models.Entry
        fields = ['tags']

    def save(self):
        entry = super(EntryTagForm, self).save()
        # create tag notifications
        models.TagNotification.create_from_entry(entry)
        return entry


class PathCreateUpdateForm(TenancyModelForm):
    tags = TagField(required=False)

    class Meta:
        model = models.Transition
        fields = ['current_state', 'answer', 'next_state', 'tags']

    def __init__(self, *args, **kwargs):
        super(PathCreateUpdateForm, self).__init__(*args, **kwargs)
        states = models.TreeState.objects.all()
        states = states.select_related('question').distinct().order_by('question__text')
        self.fields['current_state'].queryset = states
        self.fields['next_state'].queryset = states
        self.fields['answer'].queryset = models.Answer.objects.order_by('answer')
        self.fields['tags'].label = 'Auto tags'


class QuestionCreateUpdateForm(TenancyModelForm):

    class Meta:
        model = models.Question
        fields = ['text', 'error_response']


class StateCreateUpdateForm(TenancyModelForm):

    class Meta:
        model = models.TreeState
        fields = ['name', 'question', 'num_retries']


class SurveyCreateUpdateForm(TenancyModelForm):

    class Meta:
        model = models.Tree
        fields = ['trigger', 'root_state', 'completion_text', 'summary']

    def __init__(self, *args, **kwargs):
        super(SurveyCreateUpdateForm, self).__init__(*args, **kwargs)
        root_state = self.fields['root_state']
        root_state.label = 'First State'
        root_state.queryset = root_state.queryset.select_related('question')
        root_state.queryset = root_state.queryset.order_by('question__text')
        self.fields['summary'].widget = forms.Textarea()


class TagCreateUpdateForm(TenancyModelForm):

    class Meta:
        model = models.Tag
        fields = ['name', 'recipients']

    def __init__(self, *args, **kwargs):
        super(TagCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['recipients'] = forms.ModelMultipleChoiceField(
            required=False, widget=forms.CheckboxSelectMultiple,
            queryset=get_user_model().objects.exclude(email=''))
