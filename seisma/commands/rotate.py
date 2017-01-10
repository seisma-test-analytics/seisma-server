# -*- coding: utf-8 -*-

import logging
import datetime

from flask_script import Command


logger = logging.getLogger(__name__)


MAX_OBJECTS_AT_ONCE = 100
DEFAULT_ROTATE_FOR_DAYS = 365


db = None
current_app = None


def _import_db():
    global db
    from seisma.database import schema
    db = schema


def _import_current_app():
    global current_app
    from flask import current_app as app
    current_app = app


def _get_next_part_of_builds(from_date):
    return db.Build.query.filter(
        db.Build.date < from_date
    ).slice(0, MAX_OBJECTS_AT_ONCE).all()


def _get_next_part_of_results(build):
    return db.CaseResult.query.filter(
        db.CaseResult.build_id == build.id
    ).slice(0, MAX_OBJECTS_AT_ONCE).all()


def _delete_build(build):
    logger.info('Delete build with id={}'.format(build.id))

    md_list = db.BuildMetadata.query.filter(
        db.BuildMetadata.build_id == build.id,
    ).all()

    for md in md_list:
        md.delete()

    build.delete()


def _delete_result(result):
    logger.info('Delete case result with id={}'.format(result.id))

    md_list = db.CaseResultMetadata.query.filter(
        db.CaseResultMetadata.case_result_id == result.id,
    ).all()

    for md in md_list:
        md.delete()

    result.delete()


def rotate():
    _import_db()
    _import_current_app()

    rotate_for_days = current_app.config.get('ROTATE_FOR_DAYS', DEFAULT_ROTATE_FOR_DAYS)

    now = datetime.datetime.now()
    delta = datetime.timedelta(days=rotate_for_days)

    from_date = now - delta

    builds = _get_next_part_of_builds(from_date)

    while len(builds) != 0:
        for build in builds:

            results = _get_next_part_of_results(build)

            while len(results) != 0:
                for result in results:
                    _delete_result(result)

                results = _get_next_part_of_results(build)

            _delete_build(build)

        builds = _get_next_part_of_builds(from_date)


class RotateCommand(Command):
    """
    Rotate data in database
    """

    run = staticmethod(rotate)
