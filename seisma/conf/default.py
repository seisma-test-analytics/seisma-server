# -*- coding: utf-8 -*-

import os
import sys


# Application settings

DEBUG = False
TESTING = False


# Database settings

DATABASE = {
    'HOST': os.getenv('DATABASE_HOST', 'mysql'),
    'PORT': int(os.getenv('DATABASE_PORT', '3306')),
    'USER': os.getenv('DATABASE_USER', 'root'),
    'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
    'NAME': 'seisma',
    'POOL_SIZE': 10,
    'POOL_TIMEOUT': 10,
    'POOL_RECYCLE': 60 * 5,
    'MAX_OVERFLOW': -1,
    'SQL_LOG': False,
    'TRACK_MODIFICATIONS': False,
}

# Cache

REDIS_CACHE = {
    'HOST': os.getenv('REDIS_HOST', 'redis'),
    'PORT': int(os.getenv('REDIS_PORT', '6379')),
    'DB': int(os.getenv('REDIS_DATABASE', '0')),
    'IS_DISABLED': False,
    'MAX_CONNECTIONS': 15,
    'GET_CONNECTION_TIMEOUT': 10,
}

# Logging settings

LOGGING_SETTINGS = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '%(asctime)-15s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': sys.stderr,
            'formatter': 'basic'
        },
        'null': {
            'class': 'logging.NullHandler',
            'level': 'DEBUG'
        },
    },
    'loggers': {
        'seisma': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'flask': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'flask_sqlalchemy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'flask_migrate': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'flask_script': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'sqlalchemy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
    'root': {
        'propagate': False,
        'handlers': ['console'],
        'level': 'INFO',
    },
}


# clear results over days
ROTATE_FOR_DAYS = int(os.getenv('ROTATE_FOR_DAYS', '365'))

# max time of build in minutes
MAX_BUILD_TIMEOUT = int(os.getenv('MAX_BUILD_TIMEOUT', '60'))
