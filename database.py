import psycopg2
import logging
from psycopg2 import Error
from private.data import db_login

logging.basicConfig(level=logging.INFO)

_schema = "try_0"
_cursor = None


def access_database():
    global _cursor

    try:
        connection = psycopg2.connect(user=db_login['user'], password=db_login['password'],
                                      host=db_login['host'], port=db_login['port'],
                                      database=db_login['database'],
                                      )
        _cursor = connection.cursor()
        return True
    except (Exception, Error) as ex:
        logging.error("Connection Error: ", ex)
        return False


# noinspection SqlResolve
def get_orders():
    sql = f"""select * from {_schema}."last_orders";"""
    try:
        _cursor.execute(sql)
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
        logging.error("Order-Query Error: ", ex)
        return None


# noinspection SqlResolve
def get_products():
    sql = f"""select productid, productname from {_schema}."Products" order by productname;"""
    try:
        _cursor.execute(sql)
        product_rows = _cursor.fetchall()
        product_list = []
        for row in product_rows:
            product_list.append(
                {
                    'productid': row[0],
                    'productname': row[1]
                }
            )
        return product_list
    except (Exception, Error) as ex:
        logging.error("Product-Query error: ", ex)
        return None


# noinspection SqlResolve
def get_customers():
    sql = f"""select customerid, companyname from {_schema}."Customers" order by companyname;"""
    try:
        _cursor.execute(sql)
        customer_rows = _cursor.fetchall()
        customer_list = []
        for row in customer_rows:
            customer_list.append(
                {
                    'customerid': row[0],
                    'companyname': row[1]
                }
            )
        return customer_list
    except (Exception, Error) as ex:
        logging.error("Customer-Query error: ", ex)
        return None


# noinspection SqlResolve
def set_new_order(product, quantity, costumer):
    sql = "select new_order(%s, %s, %s);"
    try:
        _cursor.execute(sql, (product, quantity, costumer))
        row = _cursor.fetchone()
        success = row[0]
        return success
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)
        return False
