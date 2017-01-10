# -*- coding: utf-8 -*-


"""
About
-----

You will have results for last day from all commands.

Commands
--------
"""


import datetime
from http import HTTPStatus as statuses

import flask
from sqlalchemy import desc

from ...result import make_result
from ...resource import ApiResource
from ...utils import paginated_query
from ....database import schema as db


VERSION = 1

FOR_DAYS = 1


resource = ApiResource(__name__, version=VERSION)


def _get_date_from():
    return datetime.datetime.now() - datetime.timedelta(days=FOR_DAYS)


@resource.route('/dashboard/builds/running', methods=['GET'])
def get_running_builds():
    """
    .. http:get:: /dashboard/builds/running

    Get running builds.

    :return: Build Resource
    """
    query = db.Build.query.filter(
        db.Build.is_running == True,
        db.Build.date >= _get_date_from(),
    )
    query = query.order_by(desc(db.Build.date))
    query = paginated_query(query, flask.request)

    return make_result(
        query.all(),
        total_count=query.total_count,
    ), statuses.OK


@resource.route('/dashboard/builds/bad', methods=['GET'])
def get_last_failed_builds():
    """
    .. http:get:: /dashboard/builds/bad

    Get the bad builds.

    :return: Build Resource List
    """
    query = db.Build.query.filter(
        db.Build.was_success == False,
        db.Build.date >= _get_date_from(),
    )
    query = query.order_by(desc(db.Build.date))
    query = paginated_query(query, flask.request)

    return make_result(
        query.all(),
        total_count=query.total_count,
    ), statuses.OK


@resource.route('/dashboard/cases/bad', methods=['GET'])
def get_bad_cases():
    """
    .. http:get:: /dashboard/cases/bad

    Get the bad cases.

    :return: Case Result Resource List
    """
    query = db.CaseResult.query.join(db.Case).filter(
        db.CaseResult.case_id == db.Case.id,
        db.CaseResult.date >= _get_date_from(),
    )
    query = query.filter(db.CaseResult.status.in_(db.CASE_BAD_STATUSES))
    query = query.group_by(db.CaseResult.case_id)
    query = query.order_by(desc(db.CaseResult.date))
    query = paginated_query(query, flask.request)

    return make_result(
        query.all(),
        total_count=query.total_count,
    ), statuses.OK
