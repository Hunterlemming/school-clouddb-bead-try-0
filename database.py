import psycopg2
import logging
from psycopg2 import Error
from private.data import db_login

logging.basicConfig(level=logging.INFO)

_schema = "public"
_connection = None
_cursor = None


def access_database():
    global _cursor, _connection

    try:
        _connection = psycopg2.connect(user=db_login['user'], password=db_login['password'],
                                       host=db_login['host'], port=db_login['port'],
                                       database=db_login['database'],
                                       )
        _cursor = _connection.cursor()
        return True
    except (Exception, Error) as ex:
        logging.error("Connection Error: ", ex)
        return False


# noinspection SqlResolve
def get_orders():
    sql = f"""select * from last_orders;"""
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
    sql = f"""select productid, productname from Products order by productname;"""
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
    sql = f"""select customerid, firstname, lastname from Customers order by firstname;"""
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
def get_shipping_info(customer_id):
    sql = f"""select * from ShippingInfo where customerid='{customer_id}';"""
    try:
        _cursor.execute(sql)
        row = _cursor.fetchone()
        if row is None:
            return {}
        return {
            'ship_name': row[2],
            'ship_address': row[3],
            'ship_city': row[4],
            'ship_region': row[5],
            'ship_postal_code': row[6],
            'ship_country': row[7]
        }
    except (Exception, Error) as ex:
        logging.error("Shipping-Query error: ", ex)
        return {}


# noinspection SqlResolve
def check_order_possibility(product_id, quantity, customer_id):
    sql = """select check_order_possibility(%s, %s, %s);"""
    try:
        with _connection:
            _cursor.execute(sql, (product_id, quantity, customer_id))
            row = _cursor.fetchone()
            success = row[0] == 0
            return success
    except (Exception, Error) as ex:
        logging.error("Function (check_order_possibility) error: ", ex)
        return False


# noinspection SqlResolve
def get_shipping_id(customer_id):
    global _connection

    sql = """select get_shipping_id(%s);"""
    try:
        with _connection:
            _cursor.execute(sql, (customer_id,))
            row = _cursor.fetchone()
            return row[0]
    except (Exception, Error) as ex:
        logging.error("Function (get_shipping_id) error: ", ex)
        return None


# noinspection SqlResolve
def set_new_order(transaction_info):
    global _connection

    sql = """select new_order(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    try:
        with _connection:
            _cursor.execute(sql, (
                transaction_info['product_id'],
                transaction_info['quantity'],
                transaction_info['customer_id'],
                transaction_info['shipping_id'],
                transaction_info['ship_name'],
                transaction_info['ship_address'],
                transaction_info['ship_city'],
                transaction_info['ship_region'],
                transaction_info['ship_postal_code'],
                transaction_info['ship_country']
            ))
            row = _cursor.fetchone()
            for notice in _connection.notices:
                print(notice)
            success = row[0]
            return success
    except (Exception, Error) as ex:
        logging.error("Function (set_new_order) error: ", ex)
        return False
