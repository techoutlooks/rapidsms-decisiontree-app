from django import forms

from .utils import multitenancy_enabled, get_link_class_from_model


class RequiredInlineFormSet(forms.models.BaseInlineFormSet):

    def _construct_form(self, *args, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(*args, **kwargs)
        form.empty_permitted = False
        return form


class TenancyModelForm(forms.ModelForm):
    """For use with tenant-enabled objects."""

    @property
    def tenant_model_fields(self):
        return [field_name for field_name, field in self.fields.items()
                if isinstance(field, forms.ModelChoiceField)
                and hasattr(field.queryset.model, 'tenantlink')]

    def __init__(self, tenant, *args, **kwargs):
        self.tenant = tenant
        super(TenancyModelForm, self).__init__(*args, **kwargs)
        if multitenancy_enabled():
            # Limit tenant model field choices to those for the correct tenant.
            for field_name in self.tenant_model_fields:
                field = self.fields[field_name]
                field.queryset = field.queryset.filter(tenantlink__tenant=self.tenant)

    def save(self, *args, **kwargs):
        obj = super(TenancyModelForm, self).save(*args, **kwargs)
        if multitenancy_enabled():
            TenantLink = get_link_class_from_model(obj._meta.model)
            TenantLink.all_tenants.get_or_create(tenant=self.tenant, linked=obj)
        return obj
