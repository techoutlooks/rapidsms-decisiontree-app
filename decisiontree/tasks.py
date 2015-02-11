import datetime
import logging
import smtplib

from celery.task import task

from rapidsms.router.api import get_router

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict

from .models import Session, TagNotification


logger = logging.getLogger(__name__)


@task
def check_for_session_timeout():
    """
    Check sessions and send a reminder if they have not responded in
    the given threshold.
    """
    router = get_router()
    app = router.get_app('decisiontree')
    for session in Session.objects.open():
        app.tick(session)


@task
def status_update():
    logger.debug('status update task running')
    notifications = TagNotification.objects.filter(sent=False)
    notifications = notifications.select_related().order_by('tag', 'entry')
    logger.info('found {0} notifications'.format(notifications.count()))
    users = {}
    for notification in notifications:
        email = notification.user.email
        if email not in users:
            users[email] = []
        users[email].append(notification)
    for email, notifications in users.iteritems():
        tags = MultiValueDict()
        for notification in notifications:
            tags.appendlist(notification.tag, notification)
        context = {'tags': tags}
        body = render_to_string('tree/emails/digest.txt', context)
        try:
            send_mail(subject='Survey Response Report', message=body,
                      recipient_list=[email],
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      fail_silently=False)
            sent = True
        except smtplib.SMTPException, e:
            logger.exception(e)
            sent = False
        if sent:
            for notification in notifications:
                notification.sent = True
                notification.date_sent = datetime.datetime.now()
                notification.save()
            logger.info('Sent report to %s' % email)
