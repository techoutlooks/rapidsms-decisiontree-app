from django.conf import settings


NOTIFICATIONS_ENABLED =  getattr(settings, 'DECISIONTREE_NOTIFICATIONS', False)

SESSION_END_TRIGGER = getattr(settings, 'DECISIONTREE_SESSION_END_TRIGGER', 'end')

TIMEOUT = getattr(settings, 'DECISIONTREE_TIMEOUT', 300)
