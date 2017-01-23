# -*- coding: utf-8 -*-


"""
Build Resource
--------------

==============  ==============================  ========
Field name      Field description               Readonly
==============  ==============================  ========
job             Job resource                    Yes
name            Unique name                     Yes
date            Creation date                   Yes
runtime         Time of execution               Yes
fail_count      Count of failed tests           Yes
is_running      When a build is running then    Yes
                true else false.
                Status will false after first
                success call to stop a build.
tests_count     Total count of tests            Yes
error_count     Count of error tests            Yes
was_success     Was success after run or no     Yes
success_count   Count of success tests          Yes
metadata        Metadata of a build.            Yes
                Key -> value array.
==============  ==============================  ========

Commands
--------
"""


from http import HTTPStatus as statuses

import flask
from sqlalchemy import desc

from ... import string
from ...result import make_result
from ...resource import ApiResource
from ...utils import paginated_query
from ....database import schema as db
from ....constants import API_AUTO_CREATION_PARAM


VERSION = 1

SORT_DICT = {
    'date': db.Build.date,
    'title': db.Build.title,
    'runtime': db.Build.runtime,
    'error_count': db.Build.error_count,
    'fail_count': db.Build.fail_count,
    'success_count': db.Build.success_count,
    'tests_count': db.Build.tests_count,
}


resource = ApiResource(__name__, version=VERSION)


@resource.route('/jobs/<string:job_name>/builds', methods=['GET'])
def get_builds_from_job(job_name):
    """
    .. http:get:: /jobs/(string:job_name)/builds

    Get list of builds from job.

    :query string date_to: where data less or equal than value
    :query string date_from: where data more or equal than value
    :query float runtime_more: where runtime more than value
    :query float runtime_less: where runtime less than value
    :query int fail_count_more: where fail count more than value
    :query int fail_count_less: where fail count less than value
    :query int error_count_more: where error count more than value
    :query int error_count_less: where error count less than value
    :query int success_count_more: where success count more than value
    :query int success_count_less: where success count less than value
    :query boolean was_success: was success after run build, yes or no
    :query string sort_by: sort results by field

    :return: Build Resource List
    """
    job = db.Job.get_by_name(job_name)

    if job:
        filters = {
            'job_id': job.id,
            'is_running': False,
        }

        date_to = flask.request.args.get('date_to', None)
        date_from = flask.request.args.get('date_from', None)
        was_success = flask.request.args.get('was_success', None)
        runtime_more = flask.request.args.get('runtime_more', None)
        runtime_less = flask.request.args.get('runtime_less', None)
        fail_count_more = flask.request.args.get('fail_count_more', None)
        fail_count_less = flask.request.args.get('fail_count_less', None)
        error_count_more = flask.request.args.get('error_count_more', None)
        error_count_less = flask.request.args.get('error_count_less', None)
        success_count_more = flask.request.args.get('success_count_more', None)
        success_count_less = flask.request.args.get('success_count_less', None)
        sort_by = flask.request.args.get('sort_by', None)

        sort_key = SORT_DICT.get(sort_by, db.Build.date)

        if was_success is not None:
            filters['was_success'] = string.to_bool(was_success)

        query = db.Build.query.filter_by(**filters)
        query = query.order_by(desc(sort_key))

        if date_from is not None:
            date_from = string.to_datetime(date_from, no_time=True)
            query = query.filter(db.Build.date >= date_from)

        if date_to is not None:
            date_to = string.to_datetime(date_to, no_time=True, to_end_day=True)
            query = query.filter(db.Build.date <= date_to)

        if runtime_more is not None:
            query = query.filter(db.Build.runtime > string.to_float(runtime_more))
        elif runtime_less is not None:
            query = query.filter(db.Build.runtime < string.to_float(runtime_less))

        if fail_count_more is not None:
            query = query.filter(db.Build.fail_count > string.to_int(fail_count_more))
        elif fail_count_less is not None:
            query = query.filter(db.Build.fail_count < string.to_int(fail_count_less))

        if error_count_more is not None:
            query = query.filter(db.Build.error_count > string.to_int(error_count_more))
        elif error_count_less is not None:
            query = query.filter(db.Build.error_count < string.to_int(error_count_less))

        if success_count_more is not None:
            query = query.filter(db.Build.success_count > string.to_int(success_count_more))
        elif success_count_less is not None:
            query = query.filter(db.Build.success_count < string.to_int(success_count_less))

        query = paginated_query(query, flask.request)

        return make_result(
            query.all(),
            total_count=query.total_count,
        ), statuses.OK


@resource.route(
    '/jobs/<string:job_name>/builds/<string:build_name>/start',
    methods=['POST'],
    schema='start_build.post.json',
)
def start_build(job_name, build_name):
    """
    .. http:post:: /jobs/(string:job_name)/builds/(string:build_name)/start

    Start a new build.
    The mission of command is initialization a build what will glue case results.
    All statistic may be written with stop command.
    When build is created then it status is running while a build is not stopped.

    :jsonparam string title: build title (required)
    :jsonparam array metadata: dictionary with contains info about build.
        Key and value can be of string type only.

    :query string autocreation: magic param if job doesn't exists then will created new job.

    :return: Build Resource
    """
    job = db.Job.get_by_name(job_name)

    if not job and flask.request.args.get(API_AUTO_CREATION_PARAM):
        job = db.Job.create(name=job_name, title=job_name, is_active=True)

    if job:
        json = flask.request.get_json()

        data = {
            'job_id': job.id,
            'name': build_name,
            'title': json.get('title'),
            'runtime': 0.0,
            'fail_count': 0,
            'error_count': 0,
            'tests_count': 0,
            'success_count': 0,
            'is_running': True,
            'was_success': False,

        }
        metadata = json.get('metadata')

        build = db.Build.create(**data)

        if metadata:
            build.md = metadata

        return make_result(build), statuses.CREATED


@resource.route(
    '/jobs/<string:job_name>/builds/<string:build_name>/stop',
    methods=['PUT'],
    schema='stop_build.put.json',
)
def stop_build(job_name, build_name):
    """
    .. http:put:: /jobs/(string:job_name)/builds/(string:build_name)/stop

    Stop a build.
    The command is for creation statistic of a build what started earlier.
    A build will has status is_running=False after first call to the command with success.

    :jsonparam float runtime: time of execution (required)
    :jsonparam boolean was_success: was success or no (required)
    :jsonparam int tests_count: total count of tests (required)
    :jsonparam int success_count: cont of success tests (required)
    :jsonparam int fail_count: count of fail tests (required)
    :jsonparam int error_count: count of error tests (required)

    :return: Build Resource
    """
    job = db.Job.get_by_name(job_name)

    if job:
        build = db.Build.query.filter_by(
            job_id=job.id, name=build_name,
        ).first()

        if build:
            json = flask.request.get_json()

            data = {
                'is_running': False,
                'runtime': json.get('runtime'),
                'was_success': json.get('was_success'),
                'tests_count': json.get('tests_count'),
                'success_count': json.get('success_count'),
                'fail_count': json.get('fail_count'),
                'error_count': json.get('error_count'),
            }
            build.update(**data)

            return make_result(build), statuses.OK


@resource.route('/jobs/<string:job_name>/builds/<string:build_name>', methods=['GET'])
def get_build_by_name(job_name, build_name):
    """
    .. http:get:: /jobs/(string:job_name)/builds/(string:build_name)

    Get only one build by name.

    :return: Build Resource
    """
    job = db.Job.get_by_name(job_name)

    if job:
        build = db.Build.query.filter_by(
            job_id=job.id, name=build_name,
        ).first()

        if build:
            return make_result(build), statuses.OK
