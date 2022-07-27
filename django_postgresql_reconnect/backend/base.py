#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

import logging

from psycopg2 import InterfaceError
from psycopg2.extensions import STATUS_IN_TRANSACTION

from django.utils.asyncio import async_unsafe
from django.db.backends.postgresql.base import DatabaseWrapper as PgDatabaseWrapper


logger = logging.getLogger('django')


class DatabaseWrapper(PgDatabaseWrapper):

    @async_unsafe
    def create_cursor(self, name=None):
        try:
            return super().create_cursor(name)
        except InterfaceError:
            is_in_transaction = self.connection.status == STATUS_IN_TRANSACTION
            if self.settings_dict.get('RECONNECT') and (not is_in_transaction):
                logger.exception('Reconnect to the database "%s"', self.display_name)
                self.close_if_unusable_or_obsolete()
                self.connect()
                return super().create_cursor(name)
            raise
