from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
# username : password @ container이름 / db이름
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
load_dotenv(find_dotenv())

db = SQLAlchemy(app)


@dataclass
class Shop(db.Model):
    id: int
    shop_name: str
    shop_address: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    shop_name = db.Column(db.String(200))
    shop_address = db.Column(db.String(200))


@dataclass
class Order(db.Model):
    id: int
    shop: str
    address: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    shop = db.Column(db.Integer)
    address = db.Column(db.String(200))


@app.route("/api/shop")
def index():
    shops = Shop.query.all()
    return jsonify(shops)


@app.route("/api/order")
def order():
    orders = Order.query.all()
    return jsonify(orders)


@app.route("/api/order/<int:id>/deliver_finished", methods=["POST"])
def deliver_finished(id):
    publish("order_deliver_finished", id)
    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
