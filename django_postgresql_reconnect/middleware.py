#  Copyright © 2022 Ingram Micro Inc. All rights reserved.

from django_postgresql_reconnect import check_pgsql_connections


def check_pgsql_connections_middleware(get_response):
    def middleware(request):
        check_pgsql_connections()
        response = get_response(request)
        return response

    return middleware
