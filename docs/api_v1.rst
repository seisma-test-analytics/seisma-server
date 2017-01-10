
Version 1
=========


Defaults
--------

All commands what have list result can accept couple of **from** and **to** as GET params for pagination.
Also, **extra.total_count** will returned with result.

+------------------------------+-------------------------------+
|**PATH INFO PREFIX**          | /api/v1                       |
+------------------------------+-------------------------------+
| **DATE STRING FORMAT**       | YYYY-mm-dd                    |
+------------------------------+-------------------------------+
| **DATETIME STRING FORMAT**   | YYYY-mm-dd HH:MM              |
+------------------------------+-------------------------------+
| **PAGINATION FROM**          | 1                             |
+------------------------------+-------------------------------+
| **PAGINATION TO**            | 100                           |
+------------------------------+-------------------------------+


.. toctree::
    :maxdepth: 2

    api_v1_jobs
    api_v1_builds
    api_v1_cases
    api_v1_dashboard
