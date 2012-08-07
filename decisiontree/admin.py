#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin

from decisiontree import models


class TreeAdmin(admin.ModelAdmin):
    list_display = ('trigger', '_root_state', '_summary')

    def _root_state(self, obj):
        return obj.root_state.question.text
    _root_state.short_description = 'First question'

    def _summary(self, obj):
        return obj.summary
    _summary.short_description = 'Description'


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'type', 'answer', 'description')


class StateAdmin(admin.ModelAdmin):

    class TransitionInlineAdmin(admin.StackedInline):
        model = models.Transition
        fk_name = 'current_state'
        extra = 0

    list_display = ('id', 'name', '_question', 'num_retries', 'num_transitions')
    inlines = (TransitionInlineAdmin,)

    def _question(self, obj):
        return obj.question.text
    _question.short_description = 'Question'

    def num_transitions(self, obj):
        return obj.transition_set.count()


class TransitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_state', 'answer', 'next_state')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_recipients')
    
    def num_recipients(self, obj):
        return obj.recipients.count()


class TagNotificationAdmin(admin.ModelAdmin): 
    list_display = ('tag', 'user', 'entry', 'date_added', 'date_sent', 'sent')
    list_filter = ('date_added', 'sent')
    ordering = ('-date_added',)
    raw_id_fields = ('entry',)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'transition', 'text', 'sequence_id')


class SessionAdmin(admin.ModelAdmin):
    list_filter = ('canceled',)
    list_display = ('id', 'connection', 'tree', 'canceled')


admin.site.register(models.Tree, TreeAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.TreeState, StateAdmin)
admin.site.register(models.Transition, TransitionAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.TagNotification, TagNotificationAdmin)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Session, SessionAdmin)
