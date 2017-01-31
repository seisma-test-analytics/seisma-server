# -*- coding: utf-8 -*-

import re

from ..exceptions import ValidationError


DATE_FORMAT = '%Y-%m-%d'
DATE_STRING_PATTERN = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')


def date_to_string(date):
    """
    :type date: datetime.date
    """
    return date.strftime(DATE_FORMAT)


def validate_date_string(string):
    if DATE_STRING_PATTERN.search(string) is None:
        raise ValidationError(
            'Date string can be like "YYYY-MM-DD" format only',
        )
