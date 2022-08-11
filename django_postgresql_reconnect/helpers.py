#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

from django.db import connections

from django_postgresql_reconnect.backend.base import DatabaseWrapper


def check_pgsql_connections():
    for conn_name in connections:
        conn = connections[conn_name]
        if not isinstance(conn, DatabaseWrapper):
            continue
        if conn.should_reconnect() and (not conn.is_usable()):
            conn.reconnect()
