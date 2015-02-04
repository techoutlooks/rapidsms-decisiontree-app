from multitenancy.models import TenantEnabled

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AnswerLink(TenantEnabled):
    answer = models.OneToOneField('decisiontree.Answer', related_name='tenantlink')

    def __str__(self):
        return self.answer.__str__()


@python_2_unicode_compatible
class EntryLink(TenantEnabled):
    entry = models.OneToOneField('decisiontree.Entry', related_name='tenantlink')

    def __str__(self):
        return self.entry.__str__()


@python_2_unicode_compatible
class QuestionLink(TenantEnabled):
    question = models.OneToOneField(
        'decisiontree.Question', related_name='tenantlink')

    def __str__(self):
        return self.question.__str__()


@python_2_unicode_compatible
class SessionLink(TenantEnabled):
    session = models.OneToOneField(
        'decisiontree.Session', related_name='tenantlink')

    def __str__(self):
        return self.session.__str__()


@python_2_unicode_compatible
class TagLink(TenantEnabled):
    tag = models.OneToOneField(
        'decisiontree.Tag', related_name='tenantlink')

    def __str__(self):
        return self.tag.__str__()


@python_2_unicode_compatible
class TagNotificationLink(TenantEnabled):
    tag_notification = models.OneToOneField(
        'decisiontree.TagNotification', related_name='tenantlink')

    def __str__(self):
        return self.tag_notification.__str__()


@python_2_unicode_compatible
class TransitionLink(TenantEnabled):
    transition = models.OneToOneField(
        'decisiontree.Transition', related_name='tenantlink')

    def __str__(self):
        return self.transition.__str__()


@python_2_unicode_compatible
class TreeLink(TenantEnabled):
    tree = models.OneToOneField(
        'decisiontree.Tree', related_name='tenantlink')

    def __str__(self):
        return self.tree.__str__()


@python_2_unicode_compatible
class TreeStateLink(TenantEnabled):
    tree_state = models.OneToOneField(
        'decisiontree.TreeState', related_name='tenantlink')

    def __str__(self):
        return self.tree_state.__str__()
