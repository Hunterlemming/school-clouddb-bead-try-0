from flask import Flask, render_template, request
from database import access_database, get_orders, get_products, get_customers, set_new_order

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


def temp_db_test():
    products = get_customers()
    for product in products:
        print(product)


if __name__ == '__main__':
    connection_was_a_success = access_database()
    # temp_db_test()
    if connection_was_a_success:
        app.run(debug=True)
