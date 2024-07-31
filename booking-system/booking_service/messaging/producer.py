import logging

import json
import pika
from pika.exceptions import AMQPConnectionError
from booking.schemas import BookingOut

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)



class ProducerNotification:
    channel = None
    connection = None
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", port=5672)
            )
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange="services", exchange_type="direct"
            )
            self.channel.queue_declare(queue="GET_BOOKING_INFORMATION", durable=True)
            self.start_consuming()
        except AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}!!!!!!!")

    def send_booking_information_to_notification_service(self, username: str, email: str, booking: BookingOut):
        if self.connection is None:
            logger.error("RabbitMQ connection is not established.")
            return  # Можно обработать ошибку, если соединение не установлено
        data = {
            "username": username,
            "email": email,
            "booking": {
                **booking.model_dump()
            }
        }
        message_body = json.dumps(data, default=str)
        message_bytes = message_body.encode()

        self.channel.basic_publish(
            exchange='services',
            routing_key="GET_BOOKING_INFORMATION",
            body=message_bytes,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        logger.info(f"[x] Sent: {username} and {email}")

    def start_consuming(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Interrupted")
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
            logger.error(f"An exception occurred: {exc_val}")