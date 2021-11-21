import os
import pika
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
params = pika.URLParameters(os.environ.get("AMQP_URL"))

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="order",
        body=json.dumps(body),
        properties=properties,
    )
