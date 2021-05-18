from flask import Flask, render_template, request
from database import access_database, get_orders, get_products, get_customers, set_new_order, check_order_possibility, \
    get_shipping_id

app = Flask(__name__)

_transaction_info = {}


@app.route('/')
@app.route('/order_form', methods=['POST', 'GET'])
def order_form():
    return render_template('order_form.html', product_records=get_products(), cust_records=get_customers())


@app.route('/order_proc', methods=['POST', 'GET'])
def order_proc():
    if request.method == 'POST':
        success = set_new_order(
            {
                'product': _transaction_info['product_id'],
                'quantity': _transaction_info['quantity'],
                'customer': _transaction_info['customer_id'],
                'shipping_id': get_shipping_id(_transaction_info['customer_id']),
                'ship_name': request.form['name'],
                'ship_address': request.form['address'],
                'ship_city': request.form['city'],
                'ship_region': request.form['region'],
                'ship_postal_code': request.form['postal_code'],
                'ship_country': request.form['country'],
            }
        )
        if success:
            return render_template('order_list.html', success=success, order_records=get_orders())
        else:
            return render_template('order_form.html', product_records=get_products(), cust_records=get_customers())
    else:
        return render_template('order_list.html', order_records=get_orders())


@app.route('/shipping_info', methods=['POST'])
def shipping_info():
    global _transaction_info
    _transaction_info = {
        'product_id': request.form['product'],
        'quantity': request.form['qt'],
        'customer_id': request.form['customer']
    }
    print(_transaction_info)
    success = check_order_possibility(
        _transaction_info['product_id'],
        _transaction_info['quantity'],
        _transaction_info['customer_id']
    )
    if success:
        return render_template('shipping_info.html')
    else:
        return render_template('order_form.html',
                               product_records=get_products(), cust_records=get_customers(), success=False)


def initialize():
    global _transaction_info
    _transaction_info = {}


if __name__ == '__main__':
    initialize()
    connection_was_a_success = access_database()
    if connection_was_a_success:
        app.run(debug=True)
