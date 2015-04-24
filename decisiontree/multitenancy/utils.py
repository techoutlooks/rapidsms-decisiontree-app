from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q


def multitenancy_enabled():
    return "decisiontree.multitenancy" in settings.INSTALLED_APPS


def create_tenant_link(instance, tenant_id):
    """Link the instance to a tenant."""
    link_class = get_link_class_from_model(instance)
    tenant_link, _ = link_class.objects.get_or_create(linked=instance)
    tenant_link.tenant_id = tenant_id
    tenant_link.save()


def get_tenants_for_user(user):
    """Return all tenants that the user can manage."""
    from multitenancy.models import Tenant
    tenants = Tenant.objects.all()
    if not user.is_superuser:
        user_is_manager = Q(tenantrole__user=user) | Q(group__tenantrole__user=user)
        tenants = tenants.filter(user_is_manager)
    return tenants


def get_link_class_from_model(model):
    """Get the tenant link model associated with the model class."""
    # ModelClass.tenantlink is the reverse of a OneToOneField.
    # Traverse the field hierarchy to try to retrieve the link model.
    model_class = model if isinstance(model, type) else type(model)
    link_field = getattr(model_class, 'tenantlink', None)
    if link_field:
        related = getattr(link_field, 'related', None)
        if related:
            link_model = getattr(related, 'model', None)
            from decisiontree.multitenancy.models import TenantLink
            if link_model and issubclass(link_model, TenantLink):
                return link_model
    raise TypeError("This method should only be used on tenant-enabled models.")


def is_multitent_model(model):
    """Return whether the model class is for a multitenancy model."""
    try:
        get_link_class_from_model(model)
    except TypeError:
        return False
    else:
        return True


def tenancy_reverse(request, url_name, *args, **kwargs):
    """Add tenancy information to the URL reversal if multitenancy is enabled."""
    if multitenancy_enabled():
        # reverse disallows mixing *args and **kwargs.
        if args:
            args = (request.group_slug, request.tenant_slug) + tuple(args)
        else:
            kwargs.setdefault('group_slug', request.group_slug)
            kwargs.setdefault('tenant_slug', request.tenant_slug)
    return reverse(url_name, args=args, kwargs=kwargs)
