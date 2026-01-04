import pika
import json
import time
import sys
import os


def main():
    # 1. Connection Logic (with Retry)
    # RabbitMQ might take a few seconds to start, so we wait loop
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

    connection = None
    while connection is None:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitmq_host)
            )
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(5)

    channel = connection.channel()

    # 2. Declare Queue (Must match Producer)
    channel.queue_declare(queue="order_created")

    # 3. Define the Callback (What happens when a message arrives)
    def callback(ch, method, properties, body):
        print(f" [x] Received Event: {body}")

        data = json.loads(body)
        print("------------------------------------------------")
        print(f"📧 SENDING EMAIL TO USER {data['user_id']}")
        print(f"Subject: Order #{data['order_id']} Confirmed")
        print(f"Body: Thank you! Total paid: ${data['total_price']}")
        print("------------------------------------------------")

    # 4. Start Listening
    channel.basic_consume(
        queue="order_created", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
