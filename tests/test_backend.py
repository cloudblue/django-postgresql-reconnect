#  Copyright © 2025 CloudBlue. All rights reserved.

import logging
from copy import deepcopy
from unittest.mock import patch

import psycopg2
import pytest

from django.db import InterfaceError, connections, transaction
from django.db.utils import ConnectionHandler


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_reconnect_enabled(caplog):
    connection = ConnectionHandler()['default']
    connection.connect()
    connection.connection.close()

    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    assert cursor.fetchone() == (1,)
    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]
    assert 'psycopg2.InterfaceError: connection already closed' in caplog.records[0].exc_text


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_reconnect_disabled(settings):
    DATABASES = deepcopy(settings.DATABASES)
    DATABASES['default']['RECONNECT'] = False
    settings.DATABASES = DATABASES

    connection = ConnectionHandler()['default']
    connection.connect()
    connection.connection.close()

    with pytest.raises(InterfaceError) as err:
        connection.cursor()

    assert str(err.value) == 'connection already closed'


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
@pytest.mark.parametrize('savepoint', (False, True))
def test_reconnect_in_atomic_before_begin(savepoint, caplog):
    with transaction.atomic(savepoint=savepoint):
        connection = connections['default']
        connection.connect()
        connection.connection.close()
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        assert cursor.fetchone() == (1,)

    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
@pytest.mark.parametrize('savepoint', (False, True))
def test_not_reconnect_in_transaction(savepoint, caplog):
    with pytest.raises(InterfaceError) as err:
        with transaction.atomic(savepoint=savepoint):
            connection = connections['default']
            cursor = connection.cursor()
            cursor.execute('SELECT 1')
            assert cursor.fetchone() == (1,)
            connection.connection.close()
            connection.cursor()

    assert str(err.value) == 'connection already closed'


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_should_reconnect_connection_not_initialized():
    connection = connections['default']
    connection.close()
    connection.connection = None

    assert not connection.should_reconnect()


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_reconnect_on_operational_error_from_cursor(caplog):
    """OperationalError from cursor() (zombie connection) triggers reconnect."""
    from django.db.backends.postgresql.base import DatabaseWrapper as PgDatabaseWrapper

    connection = ConnectionHandler()['default']
    connection.connect()

    original_create_cursor = PgDatabaseWrapper.create_cursor
    call_count = 0

    def create_cursor_fails_once(self, name=None):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise psycopg2.OperationalError('server closed the connection unexpectedly')
        return original_create_cursor(self, name)

    with patch.object(PgDatabaseWrapper, 'create_cursor', create_cursor_fails_once):
        cursor = connection.cursor()

    cursor.execute('SELECT 1')
    assert cursor.fetchone() == (1,)
    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]


@pytest.mark.django_db(transaction=True, databases=['default', 'sqlite'])
def test_reconnect_retries_when_connect_fails_once(caplog):
    """If reconnect() → connect() fails transiently, a second attempt is made."""
    connection = ConnectionHandler()['default']
    connection.connect()
    connection.connection.close()  # simulate server-side disconnect (InterfaceError on cursor)

    original_connect = psycopg2.connect
    attempt = 0

    def connect_fails_once(*args, **kwargs):
        nonlocal attempt
        attempt += 1
        if attempt == 1:
            raise psycopg2.OperationalError('could not connect to server: Connection timed out')
        return original_connect(*args, **kwargs)

    with patch('psycopg2.connect', side_effect=connect_fails_once):
        cursor = connection.cursor()

    cursor.execute('SELECT 1')
    assert cursor.fetchone() == (1,)
    assert attempt == 2
    assert caplog.record_tuples == [
        ('django.db.backend', logging.WARNING, 'Reconnect to the database "default"'),
    ]
