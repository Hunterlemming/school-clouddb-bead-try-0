import psycopg2
import logging
from psycopg2 import Error
from private.data import db_login

logging.basicConfig(level=logging.INFO)


_cursor = None


def access_database():
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


def get_orders():
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
        logging.error("Order-Query Error: ", ex)
        return None


def get_products():
    try:
        _cursor.execute("select productid, productname from products order by productname;")
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


def get_customers():
    try:
        _cursor.execute("select customerid, companyname from customers order by companyname;")
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


def set_new_order(product, quantity, costumer):
    try:
        sql = "select new_order(%s, %s, %s);"
        _cursor.execute(sql, (product, quantity, costumer))
        row = _cursor.fetchone()
        success = row[0]
        return success
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)
        return False
