import logging
from copy import deepcopy

import pytest

from django.db import InterfaceError, connections, transaction
from django.db.utils import ConnectionHandler


@pytest.mark.django_db(transaction=True)
def test_reconnect_enabled(caplog):
    connection = ConnectionHandler()['default']
    connection.connect()
    connection.connection.close()

    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    assert cursor.fetchone() == (1,)
    assert caplog.record_tuples == [
        ('django', logging.ERROR, 'Reconnect to the database "PostgreSQL"'),
    ]
    assert 'psycopg2.InterfaceError: connection already closed' in caplog.records[0].exc_text


@pytest.mark.django_db(transaction=True)
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


@pytest.mark.django_db(transaction=True)
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
        ('django', logging.ERROR, 'Reconnect to the database "PostgreSQL"'),
    ]


@pytest.mark.django_db(transaction=True)
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
