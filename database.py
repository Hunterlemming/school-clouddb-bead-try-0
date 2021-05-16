import psycopg2
import logging
from psycopg2 import Error
from private.data import db_login

logging.basicConfig(level=logging.INFO)


_cursor = None


def get_database_tools():
    global _cursor

    try:
        connection = psycopg2.connect(user=db_login['user'], password=db_login['password'],
                                      host=db_login['host'], port=db_login['port'],
                                      database=db_login['database'])
        _cursor = connection.cursor()
        return {
            "connection": connection,
            "cursor": _cursor
        }
    except (Exception, Error) as ex:
        logging.error("Connection Error: ", ex)
        return None


def list_orders():
    global _cursor

    try:
        _cursor.execute("select * from last_orders;")
        order_rows = _cursor.fetchall()
        order_list = []
        for row in order_rows:
            order_list.append(
                {
                    'date': row[0],
                    'companyname': row[1],
                    'country': row[2],
                    'balance': row[3],
                    'productname': row[4],
                    'quantity': row[5],
                    'value': row[6],
                    'unitsinstock': row[7]
                 }
            )
        return order_list
    except (Exception, Error) as ex:
        logging.error("Connection Error: ", ex)
