"""
These signals handle creation/update of tenant links for objects that have a
derived relationship to a tenant.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from decisiontree import models as tree_models

from . import utils


@receiver(post_save, sender=tree_models.Session)
def create_session_tenant_link(sender, instance, **kwargs):
    """Infer a tenant link from the associated connection."""
    tenant_id = instance.connection.backend.tenantlink.tenant_id
    link_class = utils.get_link_class_from_model(sender)
    tenant_link, _ = link_class.all_tenants.get_or_create(linked=instance)
    tenant_link.tenant_id = tenant_id
    tenant_link.save()


@receiver(post_save, sender=tree_models.Entry)
def create_entry_tenant_link(sender, instance, **kwargs):
    """Infer a tenant link from the associated session."""
    tenant_id = instance.session.tenantlink.tenant_id
    link_class = utils.get_link_class_from_model(sender)
    tenant_link, _ = link_class.all_tenants.get_or_create(linked=instance)
    tenant_link.tenant_id = tenant_id
    tenant_link.save()


@receiver(post_save, sender=tree_models.TagNotification)
def create_tag_notification_tenant_link(sender, instance, **kwargs):
    """Infer a tenant link from the associated tag."""
    tenant_id = instance.tag.tenantlink.tenant_id
    link_class = utils.get_link_class_from_model(sender)
    tenant_link, _ = link_class.all_tenants.get_or_create(linked=instance)
    tenant_link.tenant_id = tenant_id
    tenant_link.save()
