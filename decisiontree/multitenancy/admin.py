from copy import copy

from django.contrib import admin
from django.utils.encoding import force_text

from . import utils
from .forms import RequiredInlineFormSet


def create_multitenancy_admin(model, model_admin=None, **kwargs):
    """Extend an existing model admin class with multitenancy admin utilities."""
    model_admin = model_admin or admin.ModelAdmin
    admin_name = 'Multitenancy{}'.format(type(model_admin).__name__)
    return type(admin_name, (MultitenancyAdminMixin, model_admin), kwargs)


class ByTenantListFilter(admin.SimpleListFilter):
    """Allow users to filter objects by the tenants they manage."""
    title = 'tenant'
    parameter_name = 'tenant'

    def lookups(self, request, model_admin):
        tenants = utils.get_tenants_for_user(request.user)
        lookups = [(tenant.pk, force_text(tenant)) for tenant in tenants]
        if request.user.is_superuser:
            lookups = lookups + [("", "None")]
        return lookups

    def queryset(self, request, queryset):
        if self.value() is not None:
            if not self.value():  # value == ""
                queryset = queryset.filter(tenantlink=None)
            else:
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
            if not request.user.is_superuser:
                tenants = utils.get_tenants_for_user(request.user)
                qs = kwargs.get('queryset', related_model.objects.all())
                kwargs['queryset'] = qs.filter(tenantlink__tenant__in=tenants)
        return super(MultitenancyAdminMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def get_tenant_link_inline(self, request, obj=None):
        """Return the inline class for the model's tenant link class."""
        tenant_link_model = utils.get_link_class_from_model(self.model)
        inline_name = '{}Inline'.format(tenant_link_model.__name__)
        return type(inline_name, (TenantLinkInlineMixin, admin.TabularInline), {
            'model': tenant_link_model,
        })

    def get_inline_instances(self, request, obj=None):
        """Add an inline fo the object's tenant link."""
        tenant_link_model = utils.get_link_class_from_model(self.model)
        if tenant_link_model.direct:
            link_inline = self.get_tenant_link_inline(request, obj)
            _original_inlines = copy(self.inlines)
            self.inlines = [link_inline] + list(self.inlines)
            instances = super(MultitenancyAdminMixin, self).get_inline_instances(request, obj)
            self.inlines = _original_inlines
        else:
            # Don't display the tenant link inline for models whose
            # relationship to a tenant is inferred.
            instances = super(MultitenancyAdminMixin, self).get_inline_instances(request, obj)
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
        qs = super(MultitenancyAdminMixin, self).get_queryset(request)
        if not request.user.is_superuser:
            tenants = utils.get_tenants_for_user(request.user)
            qs = qs.filter(tenantlink__tenant__in=tenants)
        return qs

    def tenant(self, obj):
        return obj.tenantlink.tenant
