import os
import json
import pika
from dotenv import load_dotenv, find_dotenv
from main import Shop, Order, db

load_dotenv(find_dotenv())

params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="restaurant")


def callback(ch, method, properties, body):
    print("Received in restaurant")
    data = json.loads(body)
    print(body)

    if properties.content_type == "shop_created":
        shop = Shop(
            id=data["id"],
            shop_name=data["shop_name"],
            shop_address=data["shop_address"],
        )
        db.session.add(shop)
        db.session.commit()

    elif properties.content_type == "shop_updated":
        shop = Shop.query.get(data["id"])
        shop.shop_name = data["shop_name"]
        shop.shop_address = data["shop_address"]
        db.session.commit()

    elif properties.content_type == "shop_deleted":
        try:
            shop = Shop.query.get(data)
            db.session.delete(shop)
            db.session.commit()
        except AttributeError:
            pass

    elif properties.content_type == "order_created":
        order = Order(
            id=data["id"],
            shop=data["shop"],
            address=data["address"],
        )
        db.session.add(order)
        db.session.commit()

    elif properties.content_type == "order_updated":
        order = Order.query.get(data["id"])
        order.shop = data["shop"]
        order.address = data["address"]
        db.session.commit()

    elif properties.content_type == "order_deleted":
        order = Order.query.get(data)
        db.session.delete(order)
        db.session.commit()


channel.basic_consume(queue="restaurant", on_message_callback=callback, auto_ack=True)

print("Started consuming")

channel.start_consuming()

channel.close()
