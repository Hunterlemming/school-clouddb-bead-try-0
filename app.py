from flask import Flask, render_template, request
from database import access_database, get_orders, get_products, get_customers, set_new_order
import logging

app = Flask(__name__)


@app.route('/')
@app.route('/order_form', methods=['POST', 'GET'])
def order_form():
    return render_template('order_form.html', product_records=get_products(), cust_records=get_customers())


@app.route('/order_proc', methods=['POST', 'GET'])
def order_proc():
    if request.method == 'POST':
        success = set_new_order(request.form['product'], request.form['qt'], request.form['customer'])
        return render_template('order_list.html', success=success, order_records=get_orders())
    else:
        return render_template('order_list.html', order_records=get_orders())


if __name__ == '__main__':
    toolkit = access_database()
    if toolkit is not None:
        connection = toolkit['connection']
        cursor = toolkit['cursor']
        logging.info("app indul...")
        app.run(debug=True)
