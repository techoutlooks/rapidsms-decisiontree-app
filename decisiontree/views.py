import csv
from StringIO import StringIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import SortedDict
from django.views.decorators.http import require_POST

from decisiontree import forms
from decisiontree.models import Answer, Entry, Question, Session, Tag, Transition, Tree, TreeState


@login_required
def index(request):
    trees = Tree.objects.select_related('root_state__question')
    trees = trees.annotate(count=Count('sessions'))
    return render(request, "tree/index.html", {
        'surveys': trees.order_by('trigger'),
    })


@login_required
def data(request, id):
    tree = get_object_or_404(Tree, pk=id)
    tag = None
    if request.method == 'POST':
        form = forms.AnswerSearchForm(request.POST, tree=tree)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            # what now?
    else:
        form = forms.AnswerSearchForm(tree=tree)

    entry_tags = Entry.tags.through.objects
    entry_tags = entry_tags.filter(entry__session__tree=tree)
    entry_tags = entry_tags.select_related('tag')
    tag_map = {}
    for entry_tag in entry_tags:
        if entry_tag.entry_id not in tag_map:
            tag_map[entry_tag.entry_id] = []
        tag_map[entry_tag.entry_id].append(entry_tag.tag)
    # pre-fetch all entries for this tree and create a map so we can
    # efficiently pair everything up in Python, rather than lots of SQL
    entries = Entry.objects.filter(session__tree=tree).select_related()
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
    stats = Transition.objects.filter(entries__session__tree=tree,
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
    return render(request, "tree/report/report.html", {
        'form': form,
        'tree': tree,
        'sessions': sessions,
        'states': states,
    })


@login_required
def recent_sessions(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)
    sessions = tree.sessions.select_related()
    return render(request, "tree/report/sessions.html", {
        'tree': tree,
        'ordered_sessions': sessions.order_by('-start_date')[:25],
    })


@login_required
def update_tree_summary(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)

    if request.method == 'POST':
        form = forms.TreeSummaryForm(request.POST, instance=tree)
        if form.is_valid():
            form.save()
            messages.info(request, 'Survey summary updated')
            url = reverse('survey-report', args=[tree.pk])
            return redirect(url)
    else:
        form = forms.TreeSummaryForm(instance=tree)
    return render(request, "tree/summary.html", {
        'form': form,
        'tree': tree,
    })


@login_required
def export(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)
    all_states = tree.get_all_states()
    loops = tree.has_loops()
    if not loops:
        output = StringIO()
        w = csv.writer(output)
        headings = ["Person", "Date"]
        headings.extend([state.question for state in all_states])
        w.writerow(headings)
        sessions = Session.objects.all().filter(tree=tree)
        for session in sessions:
            values = [str(session.connection), session.start_date]
            transitions = map((lambda x: x.transition), session.entries.all())
            states_w_transitions = {}
            for transition in transitions:
                states_w_transitions[transition.current_state] = transition
            for state in all_states:
                if states_w_transitions.has_key(state):
                    values.append(states_w_transitions[state].answer)
                else:
                    values.append("")
            w.writerow(values)
        # rewind the virtual file
        output.seek(0)
        response = HttpResponse(output.read(),
                            mimetype='application/ms-excel')
        response["content-disposition"] = "attachment; filename=%s.csv" % tree.trigger
        return response
    else:
        return render(request, "tree/index.html", {})


@login_required
@transaction.commit_on_success
def addtree(request, treeid=None):
    tree = None
    if treeid:
        tree = get_object_or_404(Tree, pk=treeid)

    if request.method == 'POST':
        form = forms.TreesForm(request.POST, instance=tree)
        if form.is_valid():
            tree = form.save()
            if treeid:
                validationMsg =("Survey successfully updated")
            else:
                validationMsg = "You have successfully inserted a Survey %s." % tree.trigger
            messages.info(request, validationMsg)
            return redirect('list-surveys')
    else:
        form = forms.TreesForm(instance=tree)

    return render(request, 'tree/survey.html', {
        'tree': tree,
        'form': form,
    })


@require_POST
@login_required
@transaction.commit_on_success
def deletetree(request, treeid):
    tree = get_object_or_404(Tree, pk=treeid)
    tree.delete()
    messages.info(request, 'Survey successfully deleted')
    return redirect('list-surveys')


@login_required
@transaction.commit_on_success
def addquestion(request, questionid=None):
    question = None
    if questionid:
        question = get_object_or_404(Question, pk=questionid)

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            if questionid:
                validationMsg =("You have successfully updated the Question")
            else:
                validationMsg = "You have successfully inserted a Question %s." % question.text
            messages.info(request, validationMsg)
            return redirect('list-questions')
    else:
        form = forms.QuestionForm(instance=question)

    return render(request, 'tree/question.html', {
        'question': question,
        'form': form,
        'questionid': questionid,
    })


@login_required
def questionlist(request):
    return render(request, 'tree/questions_list.html', {
        'questions': Question.objects.order_by('text')
    })


@require_POST
@login_required
@transaction.commit_on_success
def deletequestion(request, questionid):
    tree = get_object_or_404(Question, pk=questionid)
    tree.delete()
    messages.info(request, 'Question successfully deleted')
    return redirect('list-questions')


@login_required
@transaction.commit_on_success
def addanswer(request, answerid=None):
    answer = None
    if answerid:
        answer = get_object_or_404(Answer, pk=answerid)

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            if answerid:
                validationMsg =("You have successfully updated the Answer")
            else:
                validationMsg = "You have successfully inserted Answer %s." % answer.answer
                mycontext = {'validationMsg':validationMsg}
            messages.info(request, validationMsg)
            return redirect('answer_list')

    else:
        form = forms.AnswerForm(instance=answer)

    return render(request, 'tree/answer.html', {
        'answer': answer,
        'form': form,
        'answerid': answerid,
    })


@require_POST
@login_required
@transaction.commit_on_success
def deleteanswer(request, answerid):
    answer = get_object_or_404(Answer, pk=answerid)
    answer.delete()
    messages.info(request, 'Answer successfully deleted')
    return redirect('answer_list')


@login_required
def answerlist(request):
    return render(request, "tree/answers_list.html", {
        'answers': Answer.objects.order_by('name'),
    })


@login_required
def list_entries(request):
    """ List most recent survey activity """
    entries = Entry.objects.select_related().order_by('-time')[:25]
    return render(request, "tree/entry/list.html", {
        'entries': entries,
    })

@login_required
@transaction.commit_on_success
def update_entry(request, entry_id):
    """ Manually update survey entry tags """
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == 'POST':
        form = forms.EntryTagForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.info(request, 'Tags successfully updated')
            return redirect('survey-report', id=entry.session.tree.id)
    else:
        form = forms.EntryTagForm(instance=entry)
    return render(request, "tree/entry/edit.html", {
        'form': form,
        'entry': entry,
    })

@login_required
@transaction.commit_on_success
def addstate(request, stateid=None):
    state = None
    if stateid:
        state = get_object_or_404(TreeState, pk=stateid)

    if request.method == 'POST':
        form = forms.StateForm(request.POST, instance=state)
        if form.is_valid():
            state = form.save()
            if stateid:
                validationMsg =("State updated sucessfully")
            else:
                validationMsg = "You have successfully inserted State %s." % state.name
            messages.info(request, validationMsg)
            return redirect('state_list')
    else:
        form = forms.StateForm(instance=state)

    return render(request, 'tree/state.html', {
        'state': state,
        'form': form,
        'stateid': stateid,
    })


@login_required
def statelist(request):
    states = TreeState.objects.select_related('question').order_by('question')
    return render(request, "tree/states_list.html", {
        'states': states,
    })


@require_POST
@login_required
@transaction.commit_on_success
def deletestate(request, stateid):
    state = get_object_or_404(TreeState, pk=stateid)
    state.delete()
    messages.info(request, 'State successfully deleted')
    return redirect('state_list')


@login_required
def questionpathlist(request):
    paths = Transition.objects.select_related('current_state__question',
                                              'next_state__question',
                                              'answer')
    paths = paths.order_by('current_state__question__text')
    trans_tags = Transition.tags.through.objects
    trans_tags = trans_tags.filter(transition__in=[p.pk for p in paths])
    trans_tags = trans_tags.select_related('tag')
    path_map = {}
    for trans_tag in trans_tags:
        if trans_tag.transition_id not in path_map:
            path_map[trans_tag.transition_id] = []
        path_map[trans_tag.transition_id].append(trans_tag.tag)
    for path in paths:
        path.cached_tags = path_map.get(path.pk, [])
    return render(request, 'tree/path_list.html', {
        'paths': paths,
    })


@require_POST
@login_required
@transaction.commit_on_success
def deletepath(request, pathid):
    path = get_object_or_404(Transition, pk=pathid)
    path.delete()
    messages.info(request, 'Path successfully deleted')
    return redirect('path_list')


@login_required
@transaction.commit_on_success
def questionpath(request, pathid=None):
    path = None
    if pathid:
        path = get_object_or_404(Transition, pk=pathid)

    if request.method == 'POST':
        form = forms.PathForm(request.POST, instance=path)
        if form.is_valid():
            path = form.save()
            if pathid:
                validationMsg =("Path successfully updated")
            else:
                validationMsg = "You have successfully inserted Question Path %s." % path.id
            messages.info(request, validationMsg)
            return redirect('path_list')
    else:
        form = forms.PathForm(instance=path)

    return render(request, 'tree/path.html', {
        'path': path,
        'form': form,
        'pathid': pathid,
    })


@login_required
def list_tags(request):
    return render(request, "tree/tags/list.html", {
        'tags': Tag.objects.order_by('name'),
    })


@login_required
@transaction.commit_on_success
def create_edit_tag(request, tag_id=None):
    tag = None
    if tag_id:
        tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        form = forms.TagForm(request.POST, instance=tag)
        if form.is_valid():
            saved_tag = form.save()
            messages.info(request, 'Tag successfully saved')
            return redirect('list-tags')
    else:
        form = forms.TagForm(instance=tag)
    return render(request, "tree/tags/edit.html", {
        'tag': tag,
        'form': form,
    })


@require_POST
@login_required
@transaction.commit_on_success
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    tag.delete()
    messages.info(request, 'Tag successfully deleted')
    return redirect('list-tags')
