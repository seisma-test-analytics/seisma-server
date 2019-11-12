Test analytic server with opened rest API
=========================================


Build image
-----------

```bash
make build
```

Publish image
-------------

```bash
export DOCKER_USERNAME=<login>
export DOCKER_PASSWORD=<password>

make publish
```

Container environments
----------------------

* **PROCESSES** - number of processes
* **GREENLETS** - number of greenlets inside process
* **DATABASE_HOST** - mysql database host
* **DATABASE_PORT** - mysql database port
* **DATABASE_USER** - mysql database user
* **DATABASE_PASSWORD** - mysql database password
* **REDIS_HOST** - redis server host
* **REDIS_PORT** - redis server port
* **REDIS_DATABASE** - redis server database number
* **ROTATE_FOR_DAYS** - delete builds older days
* **MAX_BUILD_TIMEOUT** - fix running builds after expired timeout
