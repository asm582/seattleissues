from django.conf import settings


SETTINGS = {
    'THRESHOLD': 3,
    'PARTIALBYTES': 2,
    'SECRET_VERIFICATION_BYTES': 4,
    'SECRET_LENGTH': 32,
    'CACHE_ALIAS': 'pph'
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django_pph',
)

PASSWORD_HASHERS = (
    'django_pph.hashers.PolyPasswordHasher',
)

CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    # this will store non-persistent information (you can use the memcache if
    # desired
    'pph': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'pph_cache',
        'TIMEOUT': None,
    },
    # for persistent storage, only non sensitive information will be stored here
    'share_cache': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'share_table',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # set this path to a location specific to your project
            'filename': '/path/to/log.log',
            'formatter':'verbose',
        },
    },
    'loggers': {
        'django.security.PPH': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
SETTINGS.update(getattr(settings, 'PPH_SETTINGS', {}))
