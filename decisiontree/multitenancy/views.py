from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404

from .utils import multitenancy_enabled


class TenantMixin(object):
    """Mixin for generic class-based views to handle tenant-enabled objects.

    Use with:
        * ListView
        * DetailView
        * CreateView
        * UpdateView
        * DeleteView
    """

    def dispatch(self, request, *args, **kwargs):
        if multitenancy_enabled():
            from multitenancy.auth import get_user_groups, get_user_tenants
            available_groups = get_user_groups(request.user)
            self.group = get_object_or_404(available_groups, slug=kwargs['group_slug'])
            available_tenants = get_user_tenants(request.user, self.group)
            self.tenant = get_object_or_404(available_tenants, slug=kwargs['tenant_slug'])
        else:
            self.group = None
            self.tenant = None
        return super(TenantMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['group'] = self.group
        kwargs['tenant'] = self.tenant
        return super(TenantMixin, self).get_context_data(**kwargs)

    def get_queryset(self):
        """Limit queryset based on tenant if multitenancy is enabled."""
        qs = super(TenantMixin, self).get_queryset()
        if multitenancy_enabled():
            if not hasattr(self.model, 'tenantlink'):
                raise ImproperlyConfigured("TenantMixin can only be used with "
                                           "tenant-enabled models.")
            qs = qs.filter(tenantlink__tenant=self.tenant)
        return qs
