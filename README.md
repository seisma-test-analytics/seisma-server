Test analytic server with open rest API
=======================================

Requirements
------------

* OS from linux family. Should use ubuntu server from 14.04 version.
* python 3.5
* MySQL >= 5.5.X or MariaDB
* Nginx >=  0.8.40 Recommend >= 1.4.x


Install
-------

.. code-block::shell

    pip3.5 install --egg seisma

Use command "deploy" for creation env. See --help before.

.. code-block::shell

    seisma deploy

Create schema for database

.. code-block::shell

    seisma db init && seisma db migrate && seisma db upgrade


Migrate database schema to next version

.. code-block::shell

    seisma db migrate && seisma db upgrade


Checkout config
---------------

If you wish change default config you can use SEISMA_SETTINGS env from seisma.ini file by path /etc/seisma.ini after
deploy command execution.

Should import all from default config and rewrite what you need.

.. code-block::python

    from seisma.conf.default import *


Links
-----

* UI interface: https://github.com/trifonovmixail/seisma-ui
* Puppet(vagrant VM, docker container): https://github.com/trifonovmixail/seisma-puppet
