#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import logging

import pytest

from django.db import InterfaceError, connections

from django_postgresql_reconnect import check_pgsql_connections


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_connection_alive(client):
    check_pgsql_connections()
    connections['default'].cursor().execute('SELECT 1')


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_connection_closed(client, settings, caplog):
    connections['default'].connection.close()
    check_pgsql_connections()
    connections['default'].cursor().execute('SELECT 1')

    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_connection_not_usable(client, settings, mocker, caplog):
    mocker.patch.object(connections['default'], 'is_usable', return_value=False)
    check_pgsql_connections()
    connections['default'].cursor().execute('SELECT 1')

    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_connection_no_reconnect(client, mocker, caplog):
    mocker.patch.object(connections['default'], 'reconnect_enabled', return_value=False)
    connections['default'].connection.close()
    with pytest.raises(InterfaceError) as err:
        check_pgsql_connections()
        connections['default'].cursor().execute('SELECT 1')

    assert str(err.value) == 'connection already closed'


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_other_engine(client):
    connections['sqlite'].cursor().execute('SELECT 1')
