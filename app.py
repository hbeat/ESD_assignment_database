import json
import logging
from flask import Flask, request, make_response, jsonify
import MySQLdb
import sshtunnel 

app = Flask(__name__)
app.config["DEBUG"] = True

# MySQL configurations
username = 'USERNAME'
passwd = 'PASSWORD'
hostname = 'HOSTNAME'
db_name = "DBNAME"

@app.route("/")
def index():
    app.logger.info("INFO log: Some One landed!")
    return "Hello!"

@app.route("/products",methods=['GET'])
def display_data():
    app.logger.info("Some One request Product data")
    conn = MySQLdb.connect(user=username, passwd=passwd,host=hostname, port=3306, db=db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM product''')
    data = cursor.fetchall()
    # data = str(data)
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

    conn = MySQLdb.connect(user=username, passwd=passwd,host=hostname, port=3306, db=db_name)
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
##http://127.0.0.1:5000/insert?product=<product_name>&quantity=<qty>

if __name__ == '__main__':
    app.run(debug=True)
