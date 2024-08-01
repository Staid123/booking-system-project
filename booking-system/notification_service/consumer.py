import pika
import json
import logging
from pika.exceptions import AMQPConnectionError
from utils import send_email

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


class ConsumerNotification:
    channel = None
    connection = None
    def __init__(self):
        try:
            self.json_data = None
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672))
            self.channel = self.connection.channel()
            # Обьявляем точку обмена
            self.channel.exchange_declare(
                exchange="services", exchange_type="direct"
            )
            # Обьявляем очередь
            self.channel.queue_declare(queue="GET_BOOKING_INFORMATION", durable=True)
            # Связываем очередь с обменником
            self.channel.queue_bind(
                queue="GET_BOOKING_INFORMATION", 
                exchange="services", 
                routing_key="GET_BOOKING_INFORMATION"
            )
        except AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}!!!!!!!")

    def callback(self, ch, method, properties, body):
        try:
            message_str = body.decode()
            self.json_data = json.loads(message_str)
            logger.info(f" [x] Received {self.json_data['username']} and {self.json_data['email']} and {self.json_data['booking']}")
            send_email(username=self.json_data['username'], email=self.json_data['email'], booking=self.json_data['booking'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError as e:
            logger.info(f"Failed to decode JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def receive_booking_information_from_booking_service(self):
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.basic_consume(queue='GET_BOOKING_INFORMATION', on_message_callback=self.callback)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()

    def stop_consuming(self):
        if self.channel is not None:
            logger.info("STOP CONSUMING")
            self.channel.stop_consuming()
        if self.connection is not None:
            logger.info("CONNECTION CLOSED")
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_consuming()
        if exc_type:
            logging.error(f"An exception occurred: {exc_val}")


if __name__ == "__main__":
    consumer = ConsumerNotification()
    consumer.receive_booking_information_from_booking_service()
    # with ConsumerNotification() as consumer:
    #     consumer.receive_booking_information_from_booking_service()