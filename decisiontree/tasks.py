from celery.task import task

from decisiontree.models import Session


@task
def check_for_session_timeout():
    """
    Check sessions and send a reminder if they have not responded in
    the given threshold.

    Note: this requires the threadless router to run.
    """
    from threadless_router.router import Router
    router = Router()
    app = router.get_app('decisiontree')
    for session in Session.objects.filter(state__isnull=False, canceled__isnull=True):
        app.tick(session)
