import psycopg2
import logging
from psycopg2 import Error
from flask import Flask
from private.data import db_login

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user=db_login['user'], password=db_login['password'],
                                      host=db_login['host'], port=db_login['port'],
                                      database=db_login['database'])
        cursor = connection.cursor()
        logging.info("app indul...")
        if connection:
            app.run(debug=True)
    except (Exception, Error) as error:
        print("Connect Error: ", error)
