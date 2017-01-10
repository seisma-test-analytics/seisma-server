# -*- coding: utf-8 -*-

import sys
import random

from flask_script import Command


db = None


def import_db():
    global db
    from seisma.database import schema
    db = schema


def random_string(length=8):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(alpha) for _ in range(0, length))


def random_case_name():
    return '{}.{}:{}'.format(
        random_string(), random_string(), random_string(),
    )


def get_or_create_job(name):
    return db.Job.query.filter_by(name=name).first() or db.Job.create(
        name=name, title=random_string(), description=random_string(20),
    )


def create_success_build(job, cases_count):
    tests_count = cases_count

    build = db.Build.create(
        job_id=job.id,
        name=random_string(),
        title=random_string(),
        tests_count=tests_count,
        success_count=tests_count,
        fail_count=0,
        error_count=0,
        runtime=random.randint(1, 1000) * 1.5,
        was_success=True,
        is_running=False,
    )

    build.md = {
        'task link': 'http://localhost/browse/PROJECT-12345',
        'just': 'Метадаты на самом деле может не быть',
    }

    return build


def create_fail_build(job, cases_count):
    tests_count = cases_count
    success_count = tests_count - random.randint(1, 50)
    delta = tests_count - success_count
    fail_count = random.randint(1, delta)
    error_count = delta - fail_count

    build = db.Build.create(
        job_id=job.id,
        name=random_string(),
        title=random_string(),
        tests_count=tests_count,
        success_count=success_count,
        fail_count=fail_count,
        error_count=error_count,
        runtime=random.randint(1, 1000) * 1.5,
        was_success=False,
        is_running=False,
    )

    build.md = {
        'task link': 'http://localhost/browse/PROJECT-12345',
        'just': 'Метадаты на самом деле может не быть',
    }

    return build


def create_case(job, name):
    return db.Case.create(
        job_id=job.id,
        name=name,
        description=random_string(20),
    )


def create_success_case_results(build, cases):
    for case in cases:
        sys.stdout.write(case.name + ': ')
        db.CaseResult.create(
            case_id=case.id,
            build_id=build.id,
            reason=random_string(300),
            runtime=random.randint(20, 60) * 1.012 * 0.1,
            status='passed',
        )
        sys.stdout.write('passed\n')


def create_fail_case_results(build, cases):
    fail_counter = 0
    error_counter = 0

    for case in cases:
        if fail_counter < build.fail_count:
            status = 'failed'
            fail_counter += 1
        elif error_counter < build.error_count:
            status = 'error'
            error_counter += 1
        else:
            status = random.choice(('passed', 'skipped'))

        sys.stdout.write(case.name + ': ')

        db.CaseResult.create(
            case_id=case.id,
            build_id=build.id,
            reason=random_string(300) if status not in db.CASE_SUCCESS_STATUSES else '',
            runtime=random.randint(20, 60) * 1.012 * 0.1,
            status=status,
        )
        sys.stdout.write(status + '\n')


def make_fixtures():
    import_db()

    job_name = str(input('Please, enter job name (It will created if not exists): ') or random_string())
    builds_count = int(input('Please, enter count of builds, how many you wish: ') or random.randint(30, 100))

    job = get_or_create_job(job_name)
    case_names = [random_case_name() for _ in range(50, 500)]
    cases = []

    sys.stdout.write('\nPrepare cases...\n')

    for case_name in case_names:
        cases.append(create_case(job, case_name))

    for _ in range(0, builds_count):
        sys.stdout.write('Run build ')
        creator = random.choice(((create_success_build, create_fail_build)))
        build = creator(job, len(cases))
        sys.stdout.write('"' + build.name + '"' + '\n')
        if build.was_success:
            create_success_case_results(build, cases)
        else:
            create_fail_case_results(build, cases)


class UploadFixturesToDatabase(Command):
    """
    Upload fixtures to database.
    """

    run = staticmethod(make_fixtures)
