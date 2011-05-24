from threadless_router.router import Router

from decisiontree.models import Session

from celery.task import Task
from celery.registry import tasks

import logging
logger = logging.getLogger()

logging.getLogger().setLevel(logging.DEBUG)

class PeriodicTask(Task):
    """celery task to notice when we haven't gotten a response after some time
        and send a reminder.  See settings.py.example and README.rst"""
    def run(self):
        logger.critical("HEY I'm in decisiontree's PeriodicTask")
        router = Router()
        app = router.get_app('decisiontree')
        for session in Session.objects.filter(state__isnull=False,canceled__isnull=True):
            app.tick(session)
        logger.critical("HEY I'm in decisiontree's PeriodicTask... done")

tasks.register(PeriodicTask)
