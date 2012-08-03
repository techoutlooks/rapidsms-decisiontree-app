#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin

from decisiontree import models


class TransitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_state', 'answer', 'next_state')
    list_filter = ('answer',)
    ordering = ('current_state',)


class TagNotificationAdmin(admin.ModelAdmin): 
    list_display = ('id', 'user', 'tag', 'entry', 'date_added', 'sent',
                    'date_sent')
    list_filter = ('tag', 'date_added')
    ordering = ('-date_added',)
    raw_id_fields = ('entry',)


admin.site.register(models.Tree)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.TreeState)
admin.site.register(models.Transition, TransitionAdmin)
admin.site.register(models.Tag)
admin.site.register(models.TagNotification, TagNotificationAdmin)
admin.site.register(models.Entry)
admin.site.register(models.Session)
