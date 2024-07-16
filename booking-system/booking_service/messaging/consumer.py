import pika
import json
import logging
from pika.exceptions import AMQPConnectionError


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


class ConsumerAuthorization:
    channel = None
    connection = None
    def __init__(self):
        try:
            self.json_data = None
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672))
            self.channel = self.connection.channel()
            # Обьявляем точку обмена
            self.channel.exchange_declare(
                exchange="", exchange_type="direct"
            )
            # Обьявляем очередь
            self.channel.queue_declare(queue="GET_TOKEN_AND_USER", durable=True)
            # Связываем очередь с обменником
            self.channel.queue_bind(
                queue="GET_TOKEN_AND_USER", 
                xchange="", 
                routing_key="GET_TOKEN_AND_USER"
            )
        except AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}!!!!!!!")

    def callback(self, ch, method, properties, body):
        try:
            message_str = body.decode()
            self.json_data = json.loads(message_str)
            logger.info(f" [x] Received {self.json_data['token']} and {self.json_data['user']}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError as e:
            logger.info(f"Failed to decode JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def receive_user_obj_and_token_from_auth_service(self):
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='GET_TOKEN_AND_USER', on_message_callback=self.callback)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()
        return self.json_data["token"], self.json_data["user"]

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