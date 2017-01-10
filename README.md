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

    pip3.5 install --egg seisma

Use command "deploy" for creation env. See --help before.

    seisma deploy

Create schema for database

    seisma db init && seisma db migrate && seisma db upgrade


Migrate database schema to next version

    seisma db migrate && seisma db upgrade


Checkout config
---------------

If you wish change default config you can use SEISMA_SETTINGS env from seisma.ini file by path /etc/seisma.ini after
deploy command execution.

Should import all from default config and rewrite what you need.

    from seisma.conf.default import *


Links
-----

* UI interface: https://github.com/trifonovmixail/seisma-ui
* Puppet(vagrant VM, docker container): https://github.com/trifonovmixail/seisma-puppet
