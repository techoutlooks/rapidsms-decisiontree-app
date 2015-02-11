from django.conf import settings
from django.db.models import Q


def multitenancy_enabled():
    return "decisiontree.multitenancy" in settings.INSTALLED_APPS


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
    model_class = model if isinstance(model, type) else type(model)
    if not hasattr(model_class, 'tenantlink'):
        raise TypeError("This method should only be used on tenant-enabled models.")
    return model_class.tenantlink.related.model
