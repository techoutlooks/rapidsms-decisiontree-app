from django.contrib import admin

from .. import models
from ..forms import RequiredInlineFormSet


class BaseTenantLinkInline(admin.TabularInline):
    """A tenant link is required, and cannot be deleted."""

    formset = RequiredInlineFormSet

    def has_delete_permission(self, request, obj=None):
        return False


class AnswerLinkInline(BaseTenantLinkInline):
    model = models.AnswerLink


class EntryLinkInline(BaseTenantLinkInline):
    model = models.EntryLink


class QuestionLinkInline(BaseTenantLinkInline):
    model = models.QuestionLink


class SessionLinkInline(BaseTenantLinkInline):
    model = models.SessionLink


class TagNotificationLinkInline(BaseTenantLinkInline):
    model = models.TagNotificationLink


class TagLinkInline(BaseTenantLinkInline):
    model = models.TagLink


class TransitionLinkInline(BaseTenantLinkInline):
    model = models.TransitionLink


class TreeLinkInline(BaseTenantLinkInline):
    model = models.TreeLink


class TreeStateLinkInline(BaseTenantLinkInline):
    model = models.TreeStateLink
