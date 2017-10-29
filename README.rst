Insta Hack
==============================

Fetch data from pan card pic and show it to agent for checking accuracy

This Project uses Sqlite3 as database.

Getting up and running
----------------------

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Run django migrations command for creating table::

    $ python manage.py migrate

You can now run the usual Django ``runserver`` command (replace ``yourapp`` with the name of the directory containing the Django project)::

    $ python yourapp/manage.py runserver

For queue service, its needed to setup redis-server and start the redis server on port 6379.

Testing
-------

For testing, you can use these commands::
    
    $ python manage.py test
    
For panapp test, you can use this::

    $ python manage.py test panapp
