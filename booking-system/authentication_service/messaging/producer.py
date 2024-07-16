import logging

import json
import pika
from auth.schemas import UserOut
from pika.exceptions import AMQPConnectionError


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


class ProducerAuthorization:
    channel = None
    connection = None
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", port=5672)
            )
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange="", exchange_type="direct"
            )
            self.channel.queue_declare(queue="GET_TOKEN_AND_USER", durable=True)
            self.start_consuming()
        except AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}!!!!!!!")

    def send_user_object_and_token_to_services(self, token: str, user: UserOut):
        if self.connection is None:
            logger.error("RabbitMQ connection is not established.")
            return  # Можно обработать ошибку, если соединение не установлено
        user_data: dict = user.model_dump(exclude={"password_hash"})
        data = {
            "token": token,
            "user": user_data
        }
        message_body = json.dumps(data)
        message_bytes = message_body.encode()

        self.channel.basic_publish(
            exchange='',
            routing_key="GET_TOKEN_AND_USER",
            body=message_bytes,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        logger.info(f"[x] Sent: {token} and {user_data}")

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