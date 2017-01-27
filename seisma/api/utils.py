# -*- coding: utf-8 -*-

from . import string
from ..exceptions import ValidationError


DEFAULT_RECORDS_ON_PAGE = 50
MAX_RECORDS_TO_RESPONSE = 100


def _validate_from_to_params(f, t):
    if f > t:
        raise ValidationError(
            '"from" param can not be greater "to"',
        )

    if (t - f) > MAX_RECORDS_TO_RESPONSE:
        raise ValidationError(
            'Max count of objects in result is "{}"'.format(DEFAULT_RECORDS_ON_PAGE)
        )


def get_from_to_params_from_request(request):
    from_ = string.to_int(
        request.args.get('from', 1),
    )
    to_ = string.to_int(
        request.args.get('to', DEFAULT_RECORDS_ON_PAGE),
    )
    _validate_from_to_params(from_, to_)

    return from_, to_


def paginated_query(query, request):
    query.total_count = query.count()
    from_, to_ = get_from_to_params_from_request(request)

    query = query.slice(from_ - 1, to_)

    return query


def get_limit_offset_from_request(request):
    from_, to_ = get_from_to_params_from_request(request)

    offset = from_ - 1
    limit = (to_ - from_) + 1

    return limit, offset
