# -*- coding: utf-8 -*-

import logging

from flask_script import Option
from flask_script import Command


logger = logging.getLogger(__name__)


CMD_OPTIONS = (
    Option(
        '--job', '-j',
        dest='job_name',
        default=None,
        help='Job name for clean',
    ),
)


MAX_OBJECTS_AT_ONCE = 100
DEFAULT_ROTATE_FOR_DAYS = 365


db = None
current_app = None


class JobNotFound(LookupError):
    pass


def _import_db():
    global db
    from seisma.database import schema
    db = schema


def _import_current_app():
    global current_app
    from flask import current_app as app
    current_app = app


def _get_next_part_of_builds(job_name):
    if job_name:
        job = db.Job.query.filter(db.Job.name == job_name).first()

        if not job:
            raise JobNotFound(job_name)

        return db.Build.query.filter(
            db.Build.job_id == job.id
        ).slice(0, MAX_OBJECTS_AT_ONCE).all()

    return db.Build.query.slice(0, MAX_OBJECTS_AT_ONCE).all()


def _get_next_part_of_jobs():
    return db.Job.query.slice(0, MAX_OBJECTS_AT_ONCE).all()


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


def _delete_job(job):
    logger.info('Delete job with id={}'.format(job.id))

    job.delete()


def clean(job_name):
    _import_db()
    _import_current_app()

    builds = _get_next_part_of_builds(job_name)

    while len(builds) != 0:
        for build in builds:

            results = _get_next_part_of_results(build)

            while len(results) != 0:
                for result in results:
                    _delete_result(result)

                results = _get_next_part_of_results(build)

            _delete_build(build)

        builds = _get_next_part_of_builds(job_name)

    jobs = _get_next_part_of_jobs()

    while len(jobs) != 0:
        for job in jobs:
            _delete_job(job)

        jobs = _get_next_part_of_jobs()


class CleanCommand(Command):
    """
    Clean data in database
    """

    option_list = CMD_OPTIONS

    run = staticmethod(clean)
