# -*- coding: utf-8 -*-

import datetime
from http import HTTPStatus as statuses

import flask

from ...result import make_result
from ...resource import ApiResource
from ....database.utils import date_to_string
from ....database.alchemy import get_connection
from ...utils import get_limit_offset_from_request
from ....database.utils import validate_date_string


VERSION = 1

resource = ApiResource(__name__, version=VERSION)


@resource.route('/statistics/cases/fails', methods=['GET'])
def get_stat_about_fail_cases():
    """
    .. http:get:: /statistics/cases/fails

    Get stat about fail cases.

    :query string date_from: range from date

    :return: {
        "name": "case name",
        "fails": num of fails,
        "job": "{"name": job name", "title": "job title"}
    }
    """
    default_delta_days = 3
    date_from = flask.request.args.get('date_from', None)

    if date_from is None:
        date_from = date_to_string(
            datetime.datetime.now() - datetime.timedelta(days=default_delta_days)
        )
    else:
        validate_date_string(date_from)

    connection = get_connection()
    limit, offset = get_limit_offset_from_request(flask.request)

    subquery = """
    SELECT
        count(id)
    FROM
        `case_result` as r
    WHERE
        r.case_id=c.id
        AND
        r.date>="{date_from}"
        AND
        r.status IN ("failed", "error")
    """.format(
        date_from=date_from,
    )

    base_query = """
    SELECT
        c.name as case_name,
        j.name as job_name,
        j.title as job_title,
        ({subquery}) as fails
    FROM
        `case` as c
    JOIN
        `job` as j ON c.job_id=j.id
    ORDER BY
        fails desc
    """.format(
        subquery=subquery,
    )

    result = connection.execute(
        """
        {query}
        LIMIT {limit}
        OFFSET {offset}
        """.format(
            limit=limit,
            offset=offset,
            query=base_query,
        )
    )
    total_count = connection.execute(
        'SELECT count(*) FROM ({query}) records'.format(query=base_query)
    ).scalar()

    def formatter():
        return [
            {
                'name': r['case_name'],
                'fails': r['fails'],
                'job': {
                    'name': r['job_name'],
                    'title': r['job_title'],
                },
            }
            for r in result
        ]

    return make_result(
        formatter,
        total_count=total_count
    ), statuses.OK
