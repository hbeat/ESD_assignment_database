import json
import logging
from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.config["DEBUG"] = True

# MySQL configurations
username = 'heartbeat'
passwd = 'YOURPASSWORD'
hostname = 'DATABASEHOSTNAME'
db_name = "DBNAME"

@app.route("/")
def index():
    app.logger.info("INFO log: Some One landed!")
    return "Hello!"

@app.route("/products",methods=['GET'])
def display_data():
    app.logger.info("Some One request Product data")
    conn = MySQLdb.connect(host=hostname, user=username, passwd=passwd, db=db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM product''')
    data = cursor.fetchall()
    cursor.close()

    products = []
    quantities = []

    for row in data:
        products.append(row[0])
        quantities.append(row[1])
    jsonbody = {
        "products" : products,#["Eno","Tiffy","Para","stepsil","or"],
        "quantities": quantities,
    }
    return jsonify(jsonbody)

@app.route("/save")
def save_data():
    product = request.args.get("product")
    jsonbody = {
        "product" : product,
    }
    return jsonify(jsonbody)

@app.route("/insert")
def insert_data():
    product = request.args.get("product")
    quantity = request.args.get("quantity")

    conn = MySQLdb.connect(host=hostname, user=username, passwd=passwd, db=db_name)
    cursor = conn.cursor()
    query = '''INSERT INTO product VALUES ('{}',{});'''.format(product,int(quantity))
    cursor.execute(query)

    conn.commit()
    cursor.close()
    jsonbody = {
        "product" : product,
        "qunatity" : quantity,
    }

    return jsonify(jsonbody)
##http://localhost/insert?product=<product_name>&quantity=<qty>

if __name__ == '__main__':
    app.run(debug=True)
