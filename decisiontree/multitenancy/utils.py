from django.conf import settings


def multitenancy_enabled():
    return "decisiontree.multitenancy" in settings.INSTALLED_APPS
