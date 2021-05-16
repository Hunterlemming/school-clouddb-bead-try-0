import psycopg2
import logging
from psycopg2 import Error
from private.data import db_login

logging.basicConfig(level=logging.INFO)


def get_database_tools():
    try:
        connection = psycopg2.connect(user=db_login['user'], password=db_login['password'],
                                      host=db_login['host'], port=db_login['port'],
                                      database=db_login['database'])
        cursor = connection.cursor()
        return {
            "connection": connection,
            "cursor": cursor
        }
    except (Exception, Error) as ex:
        logging.error("Connection Error: ", ex)
        return None
