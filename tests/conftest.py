#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import os

import pytest

from django.conf import settings
from django.db import connections


def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django_postgresql_reconnect.backend',
                'NAME': 'django_postgresql_reconnect',
                'USER': os.getenv('POSTGRES_USER', 'postgres'),
                'PASSWORD': os.getenv('POSTGRES_PASSWORD', '1q2w3e'),
                'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
                'RECONNECT': True,
            },
            'sqlite': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        SECRET_KEY='secret',
    )


@pytest.fixture(autouse=True)
def renew_connections():
    for conn_name in connections:
        connections[conn_name].close()
        connections[conn_name].connect()
