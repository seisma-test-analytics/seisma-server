How to aggregate statistics
===========================

Seisma API is open and does'n require authorization.



Create job
----------

Job is parent object for builds and cases

::

   >> curl -X POST -H "Content-Type: application/json" -d '{"description": "job description", "title": "job title"}' 'http://127.0.0.1:5000/api/v1/jobs/myjob'

   {
      "result": {
         "created": "2016-09-20",
         "title": "job title",
         "description": "job description",
         "name": "myjob"
      },
      "extra": {
         "location": "/api/v1/jobs/myjob"
      }
   }




Add case to job
---------------

::

   >> curl -X POST -H "Content-Type: application/json" -d '{"description": "case description"}' 'http://127.0.0.1:5000/api/v1/jobs/myjob/cases/mycase'

   {
      "result": {
         "created": "2016-09-20",
         "description": "case description",
         "name": "mycase"
      },
      "extra": {
         "location": "/api/v1/jobs/myjob/cases/mycase"
      }
   }


Start build
-----------

If you wanna skip creation job step use GET param **autocreation=1**

::

   curl -X POST -H "Content-Type: application/json" -d '{"title": "My first build", "metadata": {"issue": "PROJECT-123"}}' 'http://127.0.0.1:5000/api/v1/jobs/myjob/builds/mybuild/start'

   {
      "result": {
         "runtime": 0.0,
         "is_running": true,
         "date": "2016-09-20 22:25",
         "tests_count": 0,
         "name": "mybuild",
         "error_count": 0,
         "was_success": false,
         "title": "My first build",
         "fail_count": 0,
         "metadata": {
            "issue": "PROJECT-123"
         },
         "success_count": 0,
         "job": {
            "created": "2016-09-20",
            "title": "job title",
            "description": "job description",
            "name": "myjob"
         }
      },
      "extra": {
         "location": "/api/v1/jobs/myjob/builds/mybuild"
      }
   }


Add case result
---------------

If you wanna skip add case step use GET param **autocreation=1**

::

   curl -X POST -H "Content-Type: application/json" -d '{"status": "failed", "runtime": 0.48, "reason": "Ooops", "metadata": {"issue": "PROJECT-123"}}' 'http://127.0.0.1:5000/api/v1/jobs/myjob/builds/mybuild/cases/mycase'

   {
      "result": {
         "runtime": 0.48,
         "case": {
            "created": "2016-09-20",
            "description": "case description",
            "name": "mycase"
         },
         "date": "2016-09-20 22:32",
         "status": "failed",
         "reason": "Ooops",
         "metadata": {
            "issue": "PROJECT-123"
         }
      },
      "extra": {
         "location": "/api/v1/jobs/myjob/builds/mybuild/cases/mycase"
      }
   }


Stop build
----------

::

   curl -X PUT -H "Content-Type: application/json" -d '{"was_success": false, "tests_count": 1, "success_count": 0, "fail_count": 1, "error_count": 0, "runtime": 0.49}' 'http://127.0.0.1:5000/api/v1/jobs/myjob/builds/mybuild/stop'

   {
      "result": {
         "runtime": 0.49,
         "is_running": false,
         "date": "2016-09-20 22:25",
         "tests_count": 1,
         "name": "mybuild",
         "error_count": 0,
         "was_success": false,
         "fail_count": 1,
         "metadata": {
            "issue": "PROJECT-123"
         },
         "success_count": 0,
         "job": {
            "created": "2016-09-20",
            "title": "job title",
            "description": "job description",
            "name": "myjob"
         }
      },
      "extra": {
         "location": "/api/v1/jobs/myjob/builds/mybuild"
      }
   }
