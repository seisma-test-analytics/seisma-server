# -*- coding: utf-8 -*-


"""
Notification Resource
--------------

==============  ==============================  ========
Field name      Field description               Readonly
==============  ==============================  ========
job_id          Job resource id                 Yes
id              id                              Yes
address         Where send notification to.     No
                For example slack channel name.
type            Type of notification.           No
                Only slack is supported for now.
options         Json with options               No
                dumped to string.
==============  ==============================  ========

Commands
--------
"""

from http import HTTPStatus as statuses

import flask

from ...resource import ApiResource
from ...result import make_result
from ...utils import paginated_query
from ....constants import API_AUTO_CREATION_PARAM
from ....database import schema as db

VERSION = 1

FIELD_NAME_TO_FIELD_INSTANCE = {
    'address': db.Notification.address,
    'type': db.Notification.type,
    'options': db.Notification.options,
}

resource = ApiResource(__name__, version=VERSION)


@resource.route('/jobs/<string:job_name>/notifications', methods=['GET'])
def get_notifications_for_job(job_name):
    """
    .. http:get:: /jobs/(string:job_name)/notifications

    Get list of notifications from job.

    :return: Notification Resource List
    """
    job = db.Job.get_by_name(job_name)

    if job:
        filters = {
            'job_id': job.id,
        }

        query = db.Notification.query.filter_by(**filters)

        query = paginated_query(query, flask.request)

        return make_result(
            query.all(),
            total_count=query.total_count,
        ), statuses.OK


@resource.route(
    '/jobs/<string:job_name>/notifications',
    methods=['POST'],
    schema='notification.json',
)
def create_notification_for_job(job_name):
    """
    .. http:post:: /jobs/(string:job_name)/notifications

    Create a new notification.
    :jsonparam string type: What system send notification to?
    :jsonparam string address: Where send notification to?
    :jsonparam string(json) options: options

    :return: Notification Resource
    """
    job = db.Job.get_by_name(job_name)

    if not job and flask.request.args.get(API_AUTO_CREATION_PARAM):
        job = db.Job.create(name=job_name, title=job_name, is_active=True)

    if job:
        json = flask.request.get_json()

        data = {
            'job_id': job.id,
            'address': json.get('address'),
            'type': json.get('type'),
            'options': json.get('options'),
        }
        notification = db.Notification.create(**data)

        return make_result(notification), statuses.CREATED


@resource.route(
    '/jobs/<string:job_name>/notifications/<string:notification_id>',
    methods=['DELETE'],
)
def delete_notification(job_name, notification_id):
    """
    .. http:delete:: /jobs/(string:job_name)/notifications/(string:notifications_id)

    Delete a notification.

    :return: Notification Resource
    """
    notification = db.Notification.get_by_id(notification_id)

    if notification:
        notification.delete()
        return make_result(notification), statuses.OK


@resource.route(
    '/jobs/<string:job_name>/notifications/<string:notification_id>',
    methods=['PUT'],
    schema='notification.update.json',
)
def update_notification(job_name, notification_id):
    """
    .. http:put:: /jobs/(string:job_name)/notifications/(string:notifications_id)

    Update a build.

    :jsonparam string type: What system send notification to?
    :jsonparam string address: Where send notification to?
    :jsonparam string(json) options: options

    :return: Notification Resource
    """
    notification = db.Notification.get_by_id(notification_id)
    if notification:
        job = db.Job.get_by_name(job_name)

        if not job and flask.request.args.get(API_AUTO_CREATION_PARAM):
            job = db.Job.create(name=job_name, title=job_name, is_active=True)

        if job:
            json = flask.request.get_json()
            data = notification.to_update()
            data.update(json)
            notification.update(**data)

            return make_result(notification), statuses.CREATED


@resource.route(
    '/jobs/<string:job_name>/notifications/<string:notification_id>',
    methods=['GET'],
)
def get_notification(job_name, notification_id):
    """
    .. http:get:: /jobs/(string:job_name)/notifications/(string:notifications_id)

    Stop a build.
    The command is for creation statistic of a build what started earlier.
    A build will has status is_running=False after first call to the command with success.

    :return: Notification Resource
    """
    notification = db.Notification.get_by_id(notification_id)

    if notification:
        return make_result(notification), statuses.OK
