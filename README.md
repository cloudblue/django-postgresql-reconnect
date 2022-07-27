# Django PostgreSQL backend with reconnection support

## Introduction

In some cases (network connection lost, load balancer issues) the connection to the database is lost without giving Django a notification.
Django tries to use such a connection and gets errors because of it. For a correct recovery, we need to restart the application workers.

This backend performs a reconnection after receiving such errors.

## Install

```
$ pip install django-postgresql-reconnect
```

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django_postgresql_reconnect.backend',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'pwd',
        'HOST': 'db_host',
        'RECONNECT': True,
    },
}
```

## Testing

1. Python 3.6+
0. Install dependencies `pip install poetry && poetry install`

Check code style: `poetry run flake8`
Run tests: `poetry run pytest`

Tests reports are generated in `tests/reports`.
* `out.xml` - JUnit test results
* `coverage.xml` - Coverage xml results

To generate HTML coverage reports use:
`--cov-report html:tests/reports/cov_html`

## License

`Python RQL` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
