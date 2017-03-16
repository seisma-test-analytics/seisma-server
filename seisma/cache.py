# -*- coding: utf-8 -*-

import inspect
from functools import wraps

import flask
import redis

from . import sjson as json

# Common defaults
DEFAULT_CACHE_TIMEOUT = 60 * 10

# Redis defaults
DEFAULT_REDIS_DB = 0
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_HOST = 'localhost'
DEFAULT_REDIS_MAX_CONNECTIONS = 50
DEFAULT_REDIS_GET_CONNECTION_TIMEOUT = 20


def _create_cache_key(func, args, kwargs):
    arguments_string = '{}{}{}'.format(
        ''.join(map(lambda a: str(a), args)),
        ''.join(map(lambda i: ''.join(map(lambda a: str(a), i)), kwargs.items())),
        ''.join(map(lambda i: ''.join(map(lambda a: str(a), i)), flask.request.args.items())),
    )
    return '{}({}) {}'.format(
        func.__name__,
        inspect.getsourcefile(func),
        ''.join(sorted(arguments_string)),
    )


def _dumps(value):
    data = {
        'data': value,
        'is_tuple': isinstance(value, tuple),
    }
    return json.dumps(data)


def _loads(value):
    data = json.loads(value)

    if data['is_tuple']:
        return tuple(data['data'])

    return data['data']


class BaseProvider(object):

    __config_key__ = None

    def __init__(self, config):
        self._config = config

    def set(self, key, value, expire=DEFAULT_CACHE_TIMEOUT):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError


class Cache(object):

    def __init__(self, app, **kwargs):
        provider_class = kwargs.get('provider_class', BaseProvider)

        assert issubclass(provider_class, BaseProvider)
        assert provider_class.__config_key__ is not None

        self._config = app.config.get(provider_class.__config_key__, {})
        self._provider = provider_class(self._config)

    @property
    def config(self):
        return self._config

    @property
    def is_disabled(self):
        return self._config.get('IS_DISABLED', False)

    @is_disabled.setter
    def is_disabled(self, value):
        self._config['IS_DISABLED'] = value

    def cached(self, timeout=DEFAULT_CACHE_TIMEOUT, key=None):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if self.is_disabled:
                    return f(*args, **kwargs)

                cache_key = key or _create_cache_key(f, args, kwargs)
                cache_data = self._provider.get(cache_key)

                if cache_data:
                    return cache_data

                result = f(*args, **kwargs)
                self._provider.set(cache_key, result, expire=timeout)
                return result

            return wrapped
        return wrapper

    def set(self, *args, **kwargs):
        return self._provider.set(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._provider.get(*args, **kwargs)


class RedisProvider(BaseProvider):

    __config_key__ = 'REDIS_CACHE'

    def __init__(self, config):
        super(RedisProvider, self).__init__(config)

        db = config.get('DB', DEFAULT_REDIS_DB)
        host = config.get('HOST', DEFAULT_REDIS_HOST)
        port = config.get('PORT', DEFAULT_REDIS_PORT)

        max_connections = config.get('MAX_CONNECTIONS', DEFAULT_REDIS_MAX_CONNECTIONS)
        get_connection_timeout = config.get('GET_CONNECTION_TIMEOUT', DEFAULT_REDIS_GET_CONNECTION_TIMEOUT)

        self._redis = redis.Redis(
            connection_pool=redis.BlockingConnectionPool(
                db=db,
                host=host,
                port=port,
                timeout=get_connection_timeout,
                max_connections=max_connections,
            ),
        )

    def set(self, key, value, expire=DEFAULT_CACHE_TIMEOUT):
        cached_data = _dumps(value)
        return self._redis.set(key, cached_data, ex=expire)

    def get(self, key, default=None):
        cached_data = self._redis.get(key)
        if cached_data:
            return _loads(cached_data)
        return default
