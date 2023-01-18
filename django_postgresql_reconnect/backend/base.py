#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import logging

from django.utils.asyncio import async_unsafe
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.postgresql.base import DatabaseWrapper as PgDatabaseWrapper

try:
    from psycopg2 import InterfaceError
    from psycopg2.extensions import STATUS_IN_TRANSACTION
except ImportError as e:
    raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)


logger = logging.getLogger('django.db.backend')


class DatabaseWrapper(PgDatabaseWrapper):

    @async_unsafe
    def create_cursor(self, name=None):
        try:
            return super().create_cursor(name)
        except InterfaceError:
            if self.should_reconnect():
                self.reconnect()
                return super().create_cursor(name)
            raise

    def reconnect_enabled(self):
        return bool(self.settings_dict.get('RECONNECT'))

    def should_reconnect(self):
        if self.connection is None:
            return False
        is_in_transaction = self.connection.status == STATUS_IN_TRANSACTION
        return self.reconnect_enabled() and (not is_in_transaction)

    def reconnect(self):
        logger.exception('Reconnect to the database "%s"', self.alias)
        self.close()
        self.connection = None
        self.connect()
