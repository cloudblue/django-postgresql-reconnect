#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import pytest

from django.http import HttpResponse
from django.db import connections
from django.test import RequestFactory

import django_postgresql_reconnect


def view(request):
    cursor = connections['default'].cursor()
    cursor.execute('SELECT NOW()')
    cursor.fetchone()
    return HttpResponse('echo')


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_middleware_connection_closed(client):
    connections['default'].connection.close()
    response = django_postgresql_reconnect.middleware(view)(RequestFactory().get('/'))

    assert response.content == b'echo'
