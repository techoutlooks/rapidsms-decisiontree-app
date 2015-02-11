from multitenancy.models import TenantEnabled

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TenantLink(TenantEnabled):

    class Meta:
        abstract = True

    def __str__(self):
        return self.linked.__str__()


class AnswerLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Answer', related_name='tenantlink')


class EntryLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Entry', related_name='tenantlink')


class QuestionLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Question', related_name='tenantlink')


class SessionLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Session', related_name='tenantlink')


class TagLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Tag', related_name='tenantlink')


class TagNotificationLink(TenantLink):
    linked = models.OneToOneField('decisiontree.TagNotification', related_name='tenantlink')


class TransitionLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Transition', related_name='tenantlink')


class TreeLink(TenantLink):
    linked = models.OneToOneField('decisiontree.Tree', related_name='tenantlink')


class TreeStateLink(TenantLink):
    linked = models.OneToOneField('decisiontree.TreeState', related_name='tenantlink')
