Available Settings
==================

rapidsms-decisiontree-app has a few settings available for configuring the
behaviour.

DECISIONTREE_NOTIFICATIONS
--------------------------

Default: ``False``

If enabled this will periodically send emails based on the response tags and
the ``TagNotification`` configurations. This requires the
``rapidsms.contrib.scheduler`` app.

DECISIONTREE_SESSION_END_TRIGGER
--------------------------------

Default: ``end``

This configures a keyword which the users can use to end their question
session.  This functionality can be disabled by making this setting ``None``.

DECISIONTREE_TIMEOUT
--------------------

Default: ``300``

This is the time in seconds to wait between questions before the user is asked
the question again or the question session is abandoned. Using this setting
requires the `threadless-router
<https://github.com/caktus/rapidsms-threadless-router>`_ and `django-celery
<https://github.com/celery/django-celery>`_. You must enable this task in your
``CELERYBEAT_SCHEDULE`` in your project settings

.. code-block:: python

    from celery.schedules import crontab

    CELERYBEAT_SCHEDULE = {
        # Other periodic tasks included here
        "decisiontree-tick": {
            "task": "decisiontree.tasks.PeriodicTask",
            # How often to check sessions for timeout
            "schedule": crontab(),  # every minute
        },
    }
