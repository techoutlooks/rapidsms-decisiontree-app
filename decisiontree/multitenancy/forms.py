from django import forms


class RequiredInlineFormSet(forms.models.BaseInlineFormSet):

    def _construct_form(self, *args, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(*args, **kwargs)
        form.empty_permitted = False
        return form
