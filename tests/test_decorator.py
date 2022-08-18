#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import pytest

from django.db import connections

import django_postgresql_reconnect


@django_postgresql_reconnect.decorator
def awesome_func():
    cursor = connections['default'].cursor()
    cursor.execute('SELECT 1')
    return cursor.fetchone()


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_decorator_connection_closed(client):
    connections['default'].connection.close()
    response = awesome_func()
    assert response == (1,)
