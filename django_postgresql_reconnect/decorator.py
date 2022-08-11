#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

from functools import wraps

from django_postgresql_reconnect.helpers import check_pgsql_connections


def check_pgsql_connections_decorator(f):
    """ Check PostgreSQL connection before running function

        import django_postgresql_reconnect

        @django_postgresql_reconnect.decorator
        def some_func():
            ...
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        check_pgsql_connections()
        return f(*args, **kwargs)
    return wrap
