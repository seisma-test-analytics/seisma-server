# -*- coding: utf-8 -*-

import datetime

from flask_script import Command


DEFAULT_BUILD_TIMEOUT = 60


def fix_aborted():
    from flask import current_app
    from seisma.database import schema as db

    now = datetime.datetime.now()
    timeout = current_app.config.get(
        'MAX_BUILD_TIMEOUT', DEFAULT_BUILD_TIMEOUT,
    )
    from_time = now - datetime.timedelta(minutes=timeout)

    builds = db.Build.query.filter(
        db.Build.is_running == True,
        db.Build.date <= from_time,
    )

    for build in builds:
        results_query = db.CaseResult.query.filter(
            db.CaseResult.build_id == build.id
        )

        tests_count = results_query.count()
        fail_count = results_query.filter(
            db.CaseResult.status == 'failed',
        ).count()
        error_count = results_query.filter(
            db.CaseResult.status == 'error',
        ).count()
        success_count = results_query.filter(
            db.CaseResult.status == 'passed',
        ).count()

        build.update(
            is_running=False,
            was_success=False,
            fail_count=fail_count,
            error_count=error_count,
            tests_count=tests_count,
            success_count=success_count,
        )


class FixAbortedBuilds(Command):
    """
    Fix aborted builds. Set is_running = False.
    See "MAX_BUILD_TIMEOUT" option in config file.
    """

    run = staticmethod(fix_aborted)
