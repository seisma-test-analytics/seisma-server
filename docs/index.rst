Welcome to seisma api documentation
===================================


Installation
------------

::

    pip3.5 install --egg seisma


System requirements:

    * OS from linux family
    * Mysql >= 5.5.X
      You can use MariaDB it's working good.
    * Nginx >=  0.8.40
      Recommend >= 1.4.x


WSGI application
----------------

.. code-block:: python

    from seisma import wsgi

    wsgi.app


For uwsgi it looks like "seisma.wsgi:app"


Configuration
-------------

Create python file and rewrite what you need. See in seisma/conf/default.py


.. code-block:: python

    from seisma.conf.default import *


You can checkout config path with **SEISMA_SETTINGS** environment. It should be full path to file.


Auto Deploy
-----------

Seisma can create bash init.d, uwsgi and nginx config files for you. See python3.5 -m seisma deploy --help.


.. toctree::
    :maxdepth: 2

    api
    aggregate

