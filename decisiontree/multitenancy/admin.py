from copy import copy

from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text

from decisiontree import admin as tree_admin
from decisiontree import models as tree_models

from . import utils
from .forms import RequiredInlineFormSet


class ByTenantListFilter(admin.SimpleListFilter):
    """Allow users to filter objects by the tenants they manage."""
    title = 'tenant'
    parameter_name = 'tenant'

    def lookups(self, request, model_admin):
        tenants = utils.get_tenants_for_user(request.user)
        return [(tenant.pk, force_text(tenant)) for tenant in tenants]

    def queryset(self, request, queryset):
        if self.value() is not None:
            queryset = queryset.filter(tenantlink__tenant=self.value())
        return queryset


class TenantLinkInlineMixin(object):
    """Require exactly one tenant link."""
    formset = RequiredInlineFormSet

    def has_delete_permission(self, request, obj=None):
        """Tenant links cannot be deleted, though they can be modified."""
        return False


class MultitenancyAdminMixin(object):
    """Add information about the tenant to an existing model admin."""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit FK choices to objects for tenants the user manages."""
        related_model = db_field.related.parent_model
        if hasattr(related_model, 'tenantlink'):
            tenants = utils.get_tenants_for_user(request.user)
            qs = kwargs.get('queryset', related_model.objects.all())
            kwargs['queryset'] = qs.filter(tenantlink__tenant__in=tenants)
        return super(MultitenancyAdminMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    @property
    def tenant_link_model(self):
        raise ImproperlyConfigured("Implementing class must specify the "
                                   "tenant link model.")

    def get_tenant_link_inline(self, request, obj=None):
        """Return the inline class for the model's tenant link class."""
        inline_name = '{}Inline'.format(self.tenant_link_model.__name__)
        return type(inline_name, (TenantLinkInlineMixin, admin.TabularInline), {
            'model': self.tenant_link_model,
        })

    def get_inline_instances(self, request, obj=None):
        """Add an inline for the object's tenant link."""
        link_inline = self.get_tenant_link_inline(request, obj)
        _original_inlines = copy(self.inlines)
        self.inlines = [link_inline] + list(self.inlines)
        instances = super(MultitenancyAdminMixin, self).get_inline_instances(request, obj)
        self.inlines = _original_inlines
        return instances

    def get_list_display(self, request):
        """Add the tenant as the last column on the list page."""
        list_display = super(MultitenancyAdminMixin, self).get_list_display(request)
        return list(list_display) + ['tenant']

    def get_list_filter(self, request):
        """Allow filtering objects by tenant."""
        list_filter = super(MultitenancyAdminMixin, self).get_list_filter(request)
        return [ByTenantListFilter] + list(list_filter)

    def get_queryset(self, request):
        """Only show objects for tenants the user manages."""
        tenants = utils.get_tenants_for_user(request.user)
        qs = super(MultitenancyAdminMixin, self).get_queryset(request)
        return qs.filter(tenantlink__tenant__in=tenants)

    def tenant(self, obj):
        return obj.tenantlink.tenant


if utils.multitenancy_enabled():
    # Unregister tree models, and re-register them with tenant-enabled admins.
    # FIXME: This assumes that the tree models have already been registered
    # (i.e., that `decisiontree` comes before `decisiontree.multitenancy` in
    # when apps are loaded)

    tree_models = [
        (tree_models.Answer, tree_admin.AnswerAdmin),
        (tree_models.Entry, tree_admin.EntryAdmin),
        (tree_models.Question, tree_admin.QuestionAdmin),
        (tree_models.Session, tree_admin.SessionAdmin),
        (tree_models.TagNotification, tree_admin.TagNotificationAdmin),
        (tree_models.Tag, tree_admin.TagAdmin),
        (tree_models.Transition, tree_admin.TransitionAdmin),
        (tree_models.Tree, tree_admin.TreeAdmin),
        (tree_models.TreeState, tree_admin.StateAdmin),
    ]

    for model, model_admin in tree_models:
        link_model = utils.get_tenant_link_from_model(model)
        admin.site.unregister(model)
        admin_name = 'Multitenancy{}'.format(model_admin.__name__)
        ModelMultitenancyAdmin = type(admin_name, (MultitenancyAdminMixin, model_admin), {
            'tenant_link_model': link_model,
        })
        admin.site.register(model, ModelMultitenancyAdmin)
