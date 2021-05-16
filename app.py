from flask import Flask, render_template, request
from database import get_database_tools
import logging
import psycopg2
from psycopg2 import Error

app = Flask(__name__)


@app.route('/')
@app.route('/order_form', methods=['POST', 'GET'])
def order_form():
    try:
        cursor.execute("select productid, productname from products order by productname;")
        product_rows = cursor.fetchall()
        product_list = []
        for row in product_rows:
            product_list.append(
                {
                    'productid': row[0],
                    'productname': row[1]
                }
            )
        # customer combo feltöltése
        cursor.execute("select customerid, companyname from customers order by companyname;")
        cust_rows = cursor.fetchall()
        cust_list = []
        for row in cust_rows:
            cust_list.append(
                {
                    'customerid': row[0],
                    'companyname': row[1]
                }
            )
        return render_template('order_form.html', product_records=product_list, cust_records=cust_list)
    except (Exception, Error) as ex:
        logging.error("Query error: ", ex)


@app.route('/order_proc', methods=['POST', 'GET'])
def order_proc():
    try:
        if request.method == 'POST':
            sql = "select new_order(%s, %s, %s);"
            with connection:
                with connection.cursor() as c:
                    c.execute(sql, (request.form['product'], request.form['qt'], request.form['customer'],))
                    row = c.fetchone()
                    return render_template('order_list.html', success=row[0], order_records=list_orders())
        else:
            return render_template('order_list.html', order_records=list_orders())
    except (Exception, Error) as ex:
        logging.error("Query or Order error: ", ex)


def list_orders():
    try:
        cursor.execute("select * from last_orders;")
        order_rows = cursor.fetchall()
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


if __name__ == '__main__':
    toolkit = get_database_tools()
    if toolkit is not None:
        connection = toolkit['connection']
        cursor = toolkit['cursor']
        logging.info("app indul...")
        app.run(debug=True)
