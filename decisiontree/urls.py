try:
    from django.conf.urls import patterns, url
except ImportError:  # Django <1.4.
    from django.conf.urls.defaults import patterns, url

from decisiontree import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='list-surveys'),
    url(r'^(?P<id>\d+)/report/$', views.data, name='survey-report'),
    url(r'^(?P<tree_id>\d+)/summary/edit/$', views.update_tree_summary,name='update_tree_summary'),
    url(r'^(?P<tree_id>\d+)/report/sessions/$', views.recent_sessions, name='recent_sessions'),
    url(r'^entry/list/$', views.list_entries, name='list-entries'),
    url(r'^entry/(?P<entry_id>\d+)/edit/$', views.update_entry,name='update-entry'),
    url(r'^tags/list/$', views.list_tags, name='list-tags'),
    url(r'^tags/create/$', views.create_edit_tag, name='create-tag'),
    url(r'^tags/(?P<tag_id>\d+)/edit/$', views.create_edit_tag, name='edit-tag'),
    url(r'^tags/(?P<tag_id>\d+)/delete/$', views.delete_tag, name='delete-tag'),
    url(r'^data/export/(?P<tree_id>\d+)/$', views.export, name='export_tree'),
    url(r'^data/add/$', views.addtree, name='add_tree'),
    url(r'^(\d+)/$', views.addtree, name='insert_tree'),
    url(r'^delete/(\d+)/$', views.deletetree, name='delete_tree'),
    url(r'^survey/question/list/$', views.questionlist, name='list-questions'),
    url(r'^survey/question/add/$', views.addquestion, name='add_question'),
    url(r'^survey/question/update/(\d+)/$', views.addquestion, name='insert_question'),
    url(r'^survey/question/delete/(\d+)/$', views.deletequestion, name='delete_question'),
    url(r'^survey/answer/list/$', views.answerlist, name='answer_list'),
    url(r'^survey/answer/add/$', views.addanswer, name='add_answer'),
    url(r'^survey/answer/update/(\d+)/$', views.addanswer, name='insert_answer'),
    url(r'^survey/answer/delete/(\d+)/$', views.deleteanswer, name='delete_answer'),
    url(r'^survey/state/list/$', views.statelist, name='state_list'),
    url(r'^survey/state/add/$', views.addstate, name='add_state'),
    url(r'^survey/state/update/(\d+)/$', views.addstate, name='insert_state'),
    url(r'^survey/state/delete/(\d+)/$', views.deletestate, name='delete_state'),
    url(r'^survey/path/list/$', views.questionpathlist, name='path_list'),
    url(r'^survey/path/add/$', views.questionpath, name='add_path'),
    url(r'^survey/path/update/(\d+)/$', views.questionpath, name='insert_path'),
    url(r'^survey/path/delete/(\d+)/$', views.deletepath, name='delete_path'),
)
