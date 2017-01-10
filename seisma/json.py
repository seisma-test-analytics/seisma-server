# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import json as _json
from flask import request
import simplejson as _sjson
from sqlalchemy.engine.result import RowProxy

from seisma.database.alchemy import ModelMixin


DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

JSON_MIME_TYPE = 'application/json'


def json_serial(obj):
    if isinstance(obj, ModelMixin):
        return obj.to_dict()

    if isinstance(obj, RowProxy):
        return dict(obj)

    if isinstance(obj, datetime.datetime):
        return obj.strftime(DATETIME_FORMAT)

    if isinstance(obj, datetime.date):
        return obj.strftime(DATE_FORMAT)

    raise TypeError(
        'Unserializable object {} of class {}'.format(obj, obj.__class__),
    )


def dumps(obj, **kwargs):
    return _json.dumps(obj, default=json_serial, **kwargs)


def dump(fp, **kwargs):
    return _json.dump(fp, default=json_serial, **kwargs)


load = _sjson.load
loads = _sjson.loads


def is_optional_rule(rule):
    if getattr(rule, 'is_optional', None) is not None:
        if rule.is_optional:
            return True
    return False


class BaseConverterRule(object):

    def __call__(self, instance):
        raise NotImplementedError(
            '"{}" is not callable'.format(self.__class__.__name__),
        )


def create_dict(instance, rules):
    fields = tuple(filter(None, request.args.get('fields', '').split(',')))

    if fields:
        return dict(
            rule(instance)
            for rule in rules
            if any((rule.alias in fields, rule.attr_name in fields))
        )

    rules = [rule for rule in rules if not is_optional_rule(rule)]

    return dict(rule(instance) for rule in rules)


class ObjectConverter(object):

    class FromAttribute(BaseConverterRule):

        def __init__(self, attr_name, alias=None, is_optional=False):
            self.alias = alias
            self.attr_name = attr_name
            self.is_optional = is_optional

        def __call__(self, instance):
            return self.alias or self.attr_name, getattr(instance, self.attr_name)

    class FromMethod(BaseConverterRule):

        def __init__(self, method_name, alias=None, is_optional=False):
            self.alias = alias
            self.method_name = method_name
            self.is_optional = is_optional

        def __call__(self, instance):
            method = getattr(instance, self.method_name)
            return self.alias or self.method_name, method()

    class FromItem(BaseConverterRule):

        def __init__(self, item_name, alias=None, is_optional=False):
            self.alias = alias
            self.item_name = item_name
            self.is_optional = is_optional

        def __call__(self, instance):
            return self.alias or self.item_name, instance[self.item_name]

    def __init__(self, *rules, **options):
        self.rules = rules
        self.is_callable = options.get('is_callable', True)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.is_callable:
            return lambda: create_dict(instance, self.rules)

        return create_dict(instance, self.rules)
