import pika
import json


def publish_order_created(data):
    # connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    # declare queue
    channel.queue_declare(queue='order_created')
    # send message
    channel.basic_publish(
        exchange='',
        routing_key='order_created',
        body=json.dumps(data)
    )
    
    print(" [x] send order event to RabbitMQ")
    connection.close()