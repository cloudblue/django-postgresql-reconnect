import os

from django.conf import settings


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
        },
        SECRET_KEY='secret',
    )
