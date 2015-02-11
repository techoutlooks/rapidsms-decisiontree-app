from multitenancy.models import TenantEnabled

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AnswerLink(TenantEnabled):
    linked = models.OneToOneField('decisiontree.Answer', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class EntryLink(TenantEnabled):
    linked = models.OneToOneField('decisiontree.Entry', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class QuestionLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.Question', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class SessionLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.Session', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class TagLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.Tag', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class TagNotificationLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.TagNotification', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class TransitionLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.Transition', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class TreeLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.Tree', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()


@python_2_unicode_compatible
class TreeStateLink(TenantEnabled):
    linked = models.OneToOneField(
        'decisiontree.TreeState', related_name='tenantlink')

    def __str__(self):
        return self.linked.__str__()
