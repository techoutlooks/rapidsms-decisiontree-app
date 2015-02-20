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

`rapidsms-decisiontree-app` is tested on RapidSMS==0.19, Django 1.7, and
Python 2.7. There is optional support for `django-celery
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

Once installed you should include ``'decisiontree'`` in your ``INSTALLED_APPS``
setting.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'decisiontree',
        ...
    )

You'll need to create the necessary database tables::

     python manage.py migrate decisiontree

At this point data can only be viewed/changed in the Django admin. If you want
to enable this on the front-end you can include the ``decisiontree.urls`` in
your root url patterns.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^surveys/', include('decisiontree.urls')),
        ...
    ]

See the `full documentation
<http://rapidsms-decisiontree-app.readthedocs.org/>`_ for additional
configuration options.

Running the Tests
-----------------

Test requirements are listed in `requirements/tests.txt` file in the `project
source <https://github.com/caktus/rapidsms-decisiontree-app>`_. These
requirements are in addition RapidSMS and its dependencies.

After you have installed ``'rapidsms_decisiontree'`` in your project, you can
use the Django test runner to run tests against your installation::

    python manage.py test decisiontree decisiontree.multitenancy

To easily run tests against different environments that `rapidsms-decisiontree-app`
supports, download the source and navigate to the `rapidsms-decisiontree-app`
directory. From there, you can use tox to run tests against a specific
environment::

    tox -e py2.7-django1.7

Or omit the `-e` argument to run tests against all environments that
`rapidsms-decisiontree-app` supports.

To see the test coverage you can run::

    coverage run $VIRTUAL_ENV/bin/django-admin.py test decisiontree --settings=decisiontree.tests.settings
    coverage report -m

A common `.coveragerc` file is include in the repo.
