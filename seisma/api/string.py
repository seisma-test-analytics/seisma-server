# -*- coding: utf-8 -*-

import datetime

from .. import exceptions
from .. import sjson as json


def to_datetime(string, no_time=False, to_end_day=False):
    try:
        dt = datetime.datetime.strptime(
            string, json.DATE_FORMAT if no_time else json.DATETIME_FORMAT,
        )
    except ValueError as error:
        raise exceptions.ValidationError(*error.args)

    if to_end_day:
        return datetime.datetime(
            dt.year,
            dt.month,
            dt.day,
            minute=59,
            hour=23,
            second=59,
            microsecond=999999,
        )

    return dt


def to_float(value):
    try:
        return float(value)
    except ValueError:
        raise exceptions.ValidationError('"{}" is not float'.format(value))


def to_int(value):
    try:
        return int(value)
    except ValueError:
        raise exceptions.ValidationError('"{}" is not integer'.format(value))


def to_bool(value):
    if isinstance(value, str):
        value = value.lower()

    if value == 'true':
        return True
    elif value == 'false':
        return False
    elif value == '1':
        return True
    elif value == '0':
        return False

    raise exceptions.ValidationError(
        '"{}" is not in (true, false)'.format(value),
    )
