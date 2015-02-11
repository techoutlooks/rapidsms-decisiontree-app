from django.apps import apps, AppConfig
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured

from .admin import create_multitenancy_admin


class DecisionTreeMultitenancyConfig(AppConfig):
    label = "decisiontree.multitenancy"
    name = "decisiontree.multitenancy"
    verbose_name = "Decision Tree Multitenancy"

    def ready(self):
        # Ensure that app requirements are met.
        required_apps = ('decisiontree', 'multitenancy')
        if not all(apps.is_installed(req) for req in required_apps):
            raise ImproperlyConfigured(
                "Include 'decisiontree' and 'multitenancy' in your "
                "INSTALLED_APPS setting to use multitenancy with "
                "rapidsms-decisiontree.")

        # Add multitenancy utilities to the regular decision tree admin
        # classes.
        for model, model_admin in admin.site._registry.items():
            if model._meta.app_label == 'decisiontree':
                ModelMultitenancyAdmin = create_multitenancy_admin(
                    model, type(model_admin))
                admin.site.unregister(model)
                admin.site.register(model, ModelMultitenancyAdmin)
