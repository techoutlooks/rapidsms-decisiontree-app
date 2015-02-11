import csv
from StringIO import StringIO

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.datastructures import SortedDict

from .. import forms
from .. import models
from . import base


class AnswerList(base.TreeListView):
    model = models.Answer
    order_by = ['name']
    template_name = 'tree/answers_list.html'


class AnswerCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "You have successfully inserted Answer {obj.answer}"
    edit_success_message = "You have successfully updated the Answer"
    form_class = forms.AnswerCreateUpdateForm
    model = models.Answer
    success_url_name = 'answer_list'
    template_name = "tree/answer.html"


class AnswerDelete(base.TreeDeleteView):
    model = models.Answer
    success_message = "Answer successfully deleted"
    success_url_name = 'answer_list'


class EntryList(base.TreeListView):
    limit = 25
    model = models.Entry
    order_by = ['-time']
    select_related = []
    template_name = "tree/entry/list.html"


class EntryUpdate(base.TreeUpdateView):
    model = models.Entry
    form_class = forms.EntryTagForm
    success_message = "Tags successfully updated"
    success_url_name = 'survey-report'
    template_name = "tree/entry/edit.html"


class PathList(base.TreeListView):
    model = models.Transition
    order_by = ['current_state__question__text']
    select_related = ['current_state__question', 'next_state__question', 'answer', 'tags']
    template_name = "tree/path_list.html"


class PathCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "You have successfully inserted Question Path {obj.id}"
    edit_success_message = "Path successfully updated"
    form_class = forms.PathCreateUpdateForm
    model = models.Transition
    success_url_name = 'path_list'
    template_name = "tree/path.html"


class PathDelete(base.TreeDeleteView):
    model = models.Transition
    success_message = "Path successfully deleted"
    success_url_name = 'path_list'


class QuestionList(base.TreeListView):
    model = models.Question
    order_by = ['text']
    template_name = 'tree/questions_list.html'


class QuestionCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "You have successfully inserted a Question {obj.text}"
    edit_success_message = "You have successfully updated the Question"
    form_class = forms.QuestionCreateUpdateForm
    model = models.Question
    success_url_name = 'list-questions'
    template_name = 'tree/question.html'


class QuestionDelete(base.TreeDeleteView):
    model = models.Question
    success_message = "Question successfully deleted"
    success_url_name = 'list-questions'


class StateList(base.TreeListView):
    model = models.TreeState
    order_by = ['question']
    select_related = ['question']
    template_name = "tree/states_list.html"


class StateCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "You have successfully inserted State {obj.name}."
    edit_success_message = "State updated successfully"
    model = models.TreeState
    form_class = forms.StateCreateUpdateForm
    success_url_name = 'state_list'
    template_name = "tree/state.html"


class StateDelete(base.TreeDeleteView):
    model = models.TreeState
    success_message = "State successfully deleted"
    success_url_name = 'state_list'


class SurveyList(base.TreeListView):
    model = models.Tree
    order_by = ['trigger']
    select_related = ['root_state__question']
    template_name = 'tree/index.html'

    def get_queryset(self):
        return super(SurveyList, self).get_queryset().annotate(count=Count('sessions'))


class SurveyExport(base.TreeDetailView):
    model = models.Tree

    def get(self, request, *args, **kwargs):
        tree = self.get_object()
        if tree.has_loops():
            return redirect('list-surveys')
        all_states = tree.get_all_states()
        output = StringIO()
        w = csv.writer(output)
        headings = ["Person", "Date"]
        headings.extend([state.question for state in all_states])
        w.writerow(headings)
        sessions = models.Session.objects.filter(tree=tree)
        for session in sessions:
            values = [str(session.connection), session.start_date]
            transitions = map((lambda x: x.transition), session.entries.all())
            states_w_transitions = {}
            for transition in transitions:
                states_w_transitions[transition.current_state] = transition
            for state in all_states:
                if state in states_w_transitions:
                    values.append(states_w_transitions[state].answer)
                else:
                    values.append("")
            w.writerow(values)
        # rewind the virtual file
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/ms-excel')
        response["content-disposition"] = "attachment; filename=%s.csv" % tree.trigger
        return response


class SurveyReport(base.TreeDetailView):
    model = models.Tree
    template_name = "tree/report/report.html"

    def dispatch(self, request, *args, **kwargs):
        tree = self.get_object()
        tag = None
        if request.method == 'POST':
            form = forms.AnswerSearchForm(request.POST, tree=tree)
            if form.is_valid():
                tag = form.cleaned_data['tag']
                # what now?
        else:
            form = forms.AnswerSearchForm(tree=tree)
        entry_tags = models.Entry.tags.through.objects
        entry_tags = entry_tags.filter(entry__session__tree=tree)
        entry_tags = entry_tags.select_related('tag')
        tag_map = {}
        for entry_tag in entry_tags:
            if entry_tag.entry_id not in tag_map:
                tag_map[entry_tag.entry_id] = []
            tag_map[entry_tag.entry_id].append(entry_tag.tag)
        # pre-fetch all entries for this tree and create a map so we can
        # efficiently pair everything up in Python, rather than lots of SQL
        entries = models.Entry.objects.filter(session__tree=tree).select_related()
        if tag:
            entries = entries.filter(tags=tag)
        entry_map = {}
        for entry in entries:
            entry.cached_tags = tag_map.get(entry.pk, [])
            state = entry.transition.current_state
            if entry.session.pk not in entry_map:
                entry_map[entry.session.pk] = {}
            entry_map[entry.session.pk][state.pk] = entry
        states = tree.get_all_states()
        sessions = tree.sessions.select_related('connection__contact',
                                                'connection__backend')
        sessions = sessions.order_by('-start_date')
        columns = SortedDict()
        for state in states:
            columns[state.pk] = []
        # for each session, created an ordered list of (state, entry) pairs
        # using the map from above. this will ease template display.
        for session in sessions:
            session.ordered_states = []
            for state in states:
                try:
                    entry = entry_map[session.pk][state.pk]
                except KeyError:
                    entry = None
                session.ordered_states.append((state, entry))
                if entry:
                    columns[state.pk].append(entry.text)
        # count answers grouped by state
        stats = models.Transition.objects.filter(entries__session__tree=tree,
                                                 entries__in=[e.pk for e in entries])
        stats = stats.values('current_state', 'answer__name')
        stats = stats.annotate(count=Count('answer'))
        stat_map = {}
        for stat in stats:
            current_state = stat['current_state']
            answer = stat['answer__name']
            count = stat['count']
            if current_state not in stat_map:
                stat_map[current_state] = {'answers': {}, 'total': 0}
            stat_map[current_state]['answers'][answer] = count
            stat_map[current_state]['total'] += count
            stat_map[current_state]['values'] = columns[current_state]
        for state in states:
            state.stats = stat_map.get(state.pk, {})
        return self.render_to_response({
            'form': form,
            'tree': tree,
            'sessions': sessions,
            'states': states,
        })


class SurveySessions(base.TreeDetailView):
    model = models.Tree
    template_name = "tree/report/sessions.html"

    def get_context_data(self, **kwargs):
        sessions = self.object.sessions.select_related().order_by('-start_date')[:25]
        kwargs['recent_sessions'] = sessions
        return super(SurveySessions, self).get_context_data(**kwargs)


class SurveyCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "You have successfully inserted a Survey {obj.trigger}"
    edit_success_message = "Survey successfully updated"
    form_class = forms.SurveyCreateUpdateForm
    model = models.Tree
    success_url_name = 'list-surveys'
    template_name = 'tree/survey.html'


class SurveyUpdateSummary(base.TreeUpdateView):
    model = models.Tree
    form_class = forms.SurveySummaryForm
    success_message = "Survey summary updated"
    success_url_name = 'survey-report'
    template_name = "tree/summary.html"

    def get_success_url(self):
        return super(SurveyUpdateSummary, self).get_success_url(self.object.pk)


class SurveyDelete(base.TreeDeleteView):
    model = models.Tree
    success_message = "Survey successfully deleted"
    success_url_name = 'list-surveys'


class TagList(base.TreeListView):
    model = models.Tag
    order_by = ['name']
    template_name = "tree/tags/list.html"


class TagCreateUpdate(base.TreeCreateUpdateView):
    create_success_message = "Tag successfully saved"
    edit_success_message = "Tag successfully saved"
    model = models.Tag
    form_class = forms.TagCreateUpdateForm
    success_url_name = 'list-tags'
    template_name = 'tree/tags/edit.html'


class TagDelete(base.TreeDeleteView):
    model = models.Tag
    success_message = "Tag successfully deleted"
    success_url_name = 'list-tags'
