from django.apps import apps, AppConfig
from django.core.exceptions import ImproperlyConfigured


class DecisionTreeMultitenancyConfig(AppConfig):
    label = "decisiontree.multitenancy"
    name = "decisiontree.multitenancy"
    verbose_name = "Decision Tree Multitenancy"

    def ready(self):
        super(DecisionTreeMultitenancyConfig, self).ready()
        required_apps = ('decisiontree', 'multitenancy')
        if not all(apps.is_installed(req) for req in required_apps):
            raise ImproperlyConfigured(
                "Include 'decisiontree' and 'multitenancy' in your "
                "INSTALLED_APPS setting to use multitenancy with "
                "rapidsms-decisiontree.")
