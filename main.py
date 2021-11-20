from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
# username : password @ container이름 / db이름
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)


db = SQLAlchemy(app)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    shop_name = db.Column(db.String(200))
    shop_address = db.Column(db.String(200))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    shop = db.Column(db.Integer)
    address = db.Column(db.String(200))


@app.route("/")
def index():
    return "Hello Flask!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")