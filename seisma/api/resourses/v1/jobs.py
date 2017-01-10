# -*- coding: utf-8 -*-

"""
Job Resource
------------

==============  ==============================  ========
Field name      Field description               Readonly
==============  ==============================  ========
name            unique build name               Yes
title           build's title                   No
created         date string when a build        Yes
                was created (readonly)
description     description of build            No
==============  ==============================  ========

Commands
--------
"""

from http import HTTPStatus as statuses

import flask
from sqlalchemy import desc

from ...result import make_result
from ...utils import api_location
from ...resource import ApiResource
from ...utils import paginated_query
from ....database import schema as db


VERSION = 1


resource = ApiResource(__name__, version=VERSION)


@resource.route('/jobs', methods=['GET'])
def get_jobs():
    """
    .. http:get:: /jobs

    Get list of jobs.

    :return: Job Resource List
    """
    query = db.Job.query.filter_by(is_active=True)
    query = query.order_by(desc(db.Job.created))
    query = paginated_query(query, flask.request)

    return make_result(
        query.all(),
        total_count=query.total_count,
    ), statuses.OK


@resource.route('/jobs/<string:job_name>', methods=['POST'], schema='job.post.json')
def create_job(job_name):
    """
    .. http:post:: /jobs/(string:job_name)

    Create job.

    :jsonparam string title: build title (required)
    :jsonparam string description: description of job

    :return: Job Resource
    """
    json = flask.request.get_json()

    data = {
        'is_active': True,
        'name': job_name,
        'title': json.get('title'),
        'description': json.get('description', ''),
    }
    job = db.Job.create(**data)

    return make_result(
        job,
        location=api_location(
            '/jobs/{}',
            job_name,
            version=VERSION,
        ),
    ), statuses.CREATED


@resource.route('/jobs/<string:job_name>', methods=['GET'])
def get_job_by_name(job_name):
    """
    .. http:get:: /jobs/(string:job_name)

    Get only one job by name.

    :return: Job Resource
    """
    job = db.Job.get_by_name(job_name)

    if job:
        return make_result(job), statuses.OK


@resource.route('/jobs/<string:job_name>', methods=['DELETE'])
def delete_job_by_name(job_name):
    """
    .. http:delete:: /jobs/(string:job_name)

    Delete job by name.

    :return: Job Resource
    """
    job = db.Job.get_by_name(job_name)

    if job:
        job.update(is_active=False)
        return make_result(job), statuses.OK
