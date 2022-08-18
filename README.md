# Django PostgreSQL backend with reconnection support
![pyversions](https://img.shields.io/pypi/pyversions/django-postgresql-reconnect.svg)
[![PyPi Status](https://img.shields.io/pypi/v/django-postgresql-reconnect.svg)](https://pypi.org/project/ddjango-postgresql-reconnect/)
[![Docs](https://readthedocs.org/projects/django-postgresql-reconnect/badge/?version=latest)](https://readthedocs.org/projects/django-postgresql-reconnect)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=django-postgresql-reconnect&metric=coverage)](https://sonarcloud.io/dashboard?id=django-postgresql-reconnect)
[![PyPI status](https://img.shields.io/pypi/status/django-postgresql-reconnect.svg)](https://pypi.python.org/pypi/django-postgresql-reconnect/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=django-postgresql-reconnect&metric=alert_status)](https://sonarcloud.io/dashboard?id=django-postgresql-reconnect)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-postgresql-reconnect)](https://pypi.org/project/django-postgresql-reconnect/)

## Introduction

In some cases (network connection lost, load balancer issues) the connection to the database is lost without giving Django a notification.
Django tries to use such a connection and gets errors because of it. For a correct recovery, we need to restart the application workers.

## Install

```
$ pip install django-postgresql-reconnect
```

## Integration

### Handling connection issues when processing HTTP requests

```python
# settings.py

DATABASES = {
    # The database back end that performs reconnect when the connection is closed
    'default': {
        'ENGINE': 'django_postgresql_reconnect.backend',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'pwd',
        'HOST': 'db_host',
        'RECONNECT': True,
    },
}

MIDDLEWARE = [
    # Middleware checks and reconnects before processing requests
    'django_postgresql_reconnect.middleware',
    ...
]
```

### Decorator for using in other places.
For example, in management commands.
```python

import django_postgresql_reconnect

@django_postgresql_reconnect.decorator
def some_awesome_function():
    ...
```



## Testing

1. Python 3.8+
0. Install dependencies `pip install poetry && poetry install`

Check code style: `poetry run flake8`
Run tests: `poetry run pytest`

Tests reports are generated in `tests/reports`.
* `out.xml` - JUnit test results
* `coverage.xml` - Coverage xml results

To generate HTML coverage reports use:
`--cov-report html:tests/reports/cov_html`

## License

`Django PostgreSQL Reconnect` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
