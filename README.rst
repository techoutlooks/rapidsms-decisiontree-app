rapidsms-decisiontree-app
=========================

This application is a generic implementation of a decision tree, which is
completely database-configurable. Users are asked questions and respond via
SMS messages using the RapidSMS framework built on top of Django.

The original code for this application was written by `Dimagi
<http://www.dimagi.com/>`_ and is currently packaged and maintained by `Caktus
Consulting Group, LLC <http://www.caktusgroup.com/services>`_.

Requirements
------------

rapidsms-decisiontree-app is compatible with Python 2.6 and 2.7, RapidSMS
0.9.6a and Django >= 1.2. There is optional support for the `threadless-router
<https://github.com/caktus/rapidsms-threadless-router>`_ and `django-celery
<https://github.com/celery/django-celery>`_.

Features
--------

* Support for sessions (i.e. 100 different users can all go through a session
  at the same time)
* Branching logic for the series of questions
* Tree visualization
* Errors for unrecognized messages (e.g. 'i don't recognize that kind of
  fruit') and multiple retries before exiting the session

Installation
------------

The latest stable release of rapidsms-decisiontree-app can be installed from
the Python Package Index (PyPi) with `pip <http://www.pip-installer.org/>`_::

    pip install rapidsms-decisiontree-app

Once installed you should include ``decisiontree`` in your ``INSTALLED_APPS``
setting.

.. code-block:: python

    INSTALLED_APPS = (
        # Other installed apps would go here
        'decisiontree',
    )

You'll need to create the necessary database tables::

     python manage.py syncdb

rapidsms-decisiontree-app supports using `South <http://south.aeracode.org/>`_
for database migrations. If you are using South then you should migrate::

    python manage.py migrate decisiontree

At this point data can only be viewed/changed in the Django admin. If you want
to enable this on the front-end you can include the ``decisiontree.urls`` in
your root url patterns.

.. code-block:: python

    urlpatterns = patterns('',
        # Other url patterns would go here
        url(r'^decisiontree/', include('decisiontree.urls')),
    )

See the `full documentation
<http://rapidsms-decisiontree-app.readthedocs.org/>`_ for additional
configuration options.

Running the Tests
-----------------

The tests are setup to run using `tox >= 1.4 <http://tox.readthedocs.org/>`_::

    pip install tox
    # Run all test environments
    tox
    # Test only Python 2.6 and Django 1.3
    tox -e py26-1.3.X

To see the test coverage you can run::

    coverage run $VIRTUAL_ENV/bin/django-admin.py test decisiontree --settings=decisiontree.tests.settings
    coverage report -m

A common .coveragerc file is include in the repo.
