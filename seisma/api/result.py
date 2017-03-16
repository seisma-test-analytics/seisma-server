# -*- coding: utf-8 -*-

import types


def make_result(data, **extra):
    if type(data) is types.FunctionType:
        data = data()

    return {
        'result': data,
        'extra': extra,
    }


def make_error_result(messages, type=None, exc=None):
    if exc:
        type = exc.__class__.__name__
    elif not type and not exc:
        type = 'UnknownError'

    if isinstance(messages, str):
        messages = [messages]

    return {
        'type': type,
        'messages': messages,
    }
