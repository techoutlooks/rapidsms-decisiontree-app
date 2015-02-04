from django.contrib import admin as django_admin

from decisiontree import models as tree_models

from ..utils import multitenancy_enabled
from . import admin as multitenancy_admin


if multitenancy_enabled():
    django_admin.site.unregister(tree_models.Answer)
    django_admin.site.register(
        tree_models.Answer, multitenancy_admin.MultitenancyAnswerAdmin)

    django_admin.site.unregister(tree_models.Entry)
    django_admin.site.register(
        tree_models.Entry, multitenancy_admin.MultitenancyEntryAdmin)

    django_admin.site.unregister(tree_models.Question)
    django_admin.site.register(
        tree_models.Question, multitenancy_admin.MultitenancyQuestionAdmin)

    django_admin.site.unregister(tree_models.Session)
    django_admin.site.register(
        tree_models.Session, multitenancy_admin.MultitenancySessionAdmin)

    django_admin.site.unregister(tree_models.TagNotification)
    django_admin.site.register(
        tree_models.TagNotification, multitenancy_admin.MultitenancyTagNotificationAdmin)

    django_admin.site.unregister(tree_models.Tag)
    django_admin.site.register(
        tree_models.Tag, multitenancy_admin.MultitenancyTagAdmin)

    django_admin.site.unregister(tree_models.Transition)
    django_admin.site.register(
        tree_models.Transition, multitenancy_admin.MultitenancyTransitionAdmin)

    django_admin.site.unregister(tree_models.Tree)
    django_admin.site.register(
        tree_models.Tree, multitenancy_admin.MultitenancyTreeAdmin)

#    django_admin.site.unregister(tree_models.TreeState)
#    django_admin.site.register(
#        tree_models.TreeState, multitenancy_admin.MultitenancyTreeStateAdmin)
