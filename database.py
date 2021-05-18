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
                    'firstname': row[1],
                    'lastname': row[2],
                    'country': row[3],
                    'balance': row[4],
                    'productname': row[5],
                    'quantity': row[6],
                    'value': row[7],
                    'unitsinstock': row[8]
                 }
            )
        return order_list
    except (Exception, Error) as ex:
        logging.error("Order-Query Error: ", ex)
        return []


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
        return []


# noinspection SqlResolve
def get_customers():
    sql = f"""select customerid, firstname, lastname from {_schema}."Customers" order by firstname;"""
    try:
        _cursor.execute(sql)
        customer_rows = _cursor.fetchall()
        customer_list = []
        for row in customer_rows:
            customer_list.append(
                {
                    'customerid': row[0],
                    'companyname': f"{row[1]} {row[2]}"
                }
            )
        return customer_list
    except (Exception, Error) as ex:
        logging.error("Customer-Query error: ", ex)
        return []


# noinspection SqlResolve
def check_order_possibility(product_id, quantity, customer_id):
    sql = """select try_0."check_order_possibility"(%s, %s, %s);"""
    try:
        _cursor.execute(sql, (product_id, quantity, customer_id))
        row = _cursor.fetchone()
        success = row[0] == 0
        return success
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)
        return False


# noinspection SqlResolve
def get_shipping_id(customer_id):
    sql = """select try_0."get_shipping_id"(%s);"""
    try:
        _cursor.execute(sql, (customer_id,))
        row = _cursor.fetchone()
        return row[0]
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)
        return None


# noinspection SqlResolve
def set_new_order(product, quantity, costumer):
    sql = """select try_0."new_order"(%s, %s, %s);"""
    try:
        _cursor.execute(sql, (product, quantity, costumer))
        row = _cursor.fetchone()
        success = row[0]
        return success
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)
        return False
