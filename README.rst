rapidsms-decisiontree-app
==============================

This application is a generic implementation of a decision tree, which is completely database-configurable.
Users are asked questions and respond via SMS messages using the RapidSMS framework built on top of Django.

The original code for this application was written by `Dimagi <http://www.dimagi.com/>`_ and is currently
packaged and maintained by `Caktus Consulting Group, LLC <http://www.caktusgroup.com/services>`_.


Requirements
-----------------------------------

rapidsms-decisiontree-app is compatible with Python 2.6 and 2.7, RapidSMS 0.9.6a and Django >= 1.2.


Features
-----------------------------------

 * Support for sessions (i.e. 100 different users can all go through a session at the same time)
 * Branching logic for the series of questions
 * Tree visualization
 * Errors for unrecognized messages (e.g. 'i don't recognize that kind of fruit') and multiple retries before exiting the session


Running the Tests
-----------------------------------

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
