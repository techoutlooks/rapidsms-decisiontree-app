from decisiontree import admin as tree_admin

from . import inline


class MultitenancyAdminMixin(object):

    def get_list_display(self, request):
        list_display = super(MultitenancyAdminMixin, self).get_list_display(request)
        return ['tenant'] + list(list_display)

    def get_list_filter(self, request):
        list_filter = super(MultitenancyAdminMixin, self).get_list_filter(request)
        return ['tenantlink__tenant'] + list(list_filter)

    def get_queryset(self, request):
        qs = super(MultitenancyAdminMixin, self).get_queryset(request)
        # TODO: filter to only the objects that the user can see.
        return qs

    def tenant(self, obj):
        return obj.tenantlink.tenant


class MultitenancyAnswerAdmin(MultitenancyAdminMixin, tree_admin.AnswerAdmin):
    inlines = [inline.AnswerLinkInline] + list(tree_admin.AnswerAdmin.inlines)


class MultitenancyEntryAdmin(MultitenancyAdminMixin, tree_admin.EntryAdmin):
    inlines = [inline.EntryLinkInline] + list(tree_admin.EntryAdmin.inlines)


class MultitenancyQuestionAdmin(MultitenancyAdminMixin, tree_admin.QuestionAdmin):
    inlines = [inline.QuestionLinkInline] + list(tree_admin.QuestionAdmin.inlines)


class MultitenancySessionAdmin(MultitenancyAdminMixin, tree_admin.SessionAdmin):
    inlines = [inline.SessionLinkInline] + list(tree_admin.SessionAdmin.inlines)


class MultitenancyTagNotificationAdmin(MultitenancyAdminMixin, tree_admin.TagNotificationAdmin):
    inlines = [inline.TagNotificationLinkInline] + list(tree_admin.TagNotificationAdmin.inlines)


class MultitenancyTagAdmin(MultitenancyAdminMixin, tree_admin.TagAdmin):
    inlines = [inline.TagLinkInline] + list(tree_admin.TagAdmin.inlines)


class MultitenancyTransitionAdmin(MultitenancyAdminMixin, tree_admin.TransitionAdmin):
    inlines = [inline.TransitionLinkInline] + list(tree_admin.TransitionAdmin.inlines)


class MultitenancyTreeAdmin(MultitenancyAdminMixin, tree_admin.TreeAdmin):
    inlines = [inline.TreeLinkInline] + list(tree_admin.TreeAdmin.inlines)


# class MultitenancyTreeStateAdmin(MultitenancyAdminMixin, tree_admin.TreeStateAdmin):
#     inlines = [inline.TreeStateInline] + list(tree_admin.TreeStateAdmin.inlines)
