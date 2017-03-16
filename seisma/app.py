# -*- coding: utf-8 -*-

import flask

from . import constants
from . import sjson as json


class WSGIApplication(flask.Flask):

    json_decoder = json.JSONDecoder
    json_encoder = json.JSONEncoder

    def __init__(self, *args, **kwargs):
        super(WSGIApplication, self).__init__(*args, **kwargs)

        self.config.from_envvar(constants.CONFIG_ENV_NAME)

        self.init_logging()
        self.init_alchemy()
        self.init_cache()

        with self.app_context():
            self.init_blueprints()

    def init_alchemy(self):
        from seisma.database import alchemy
        alchemy.setup(self)

    def init_cache(self):
        from seisma.cache import Cache, RedisProvider
        self.cache = Cache(self, provider_class=RedisProvider)

    def init_logging(self):
        logging_settings = self.config.get('LOGGING_SETTINGS')

        if isinstance(logging_settings, dict):
            from logging.config import dictConfig
            dictConfig(logging_settings)

    def init_blueprints(self):
        from seisma import api
        from seisma import views

        api.setup(self)
        views.setup(self)

    def cached(self, *args, **kwargs):
        return self.cache.cached(*args, **kwargs)
