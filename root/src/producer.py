import json
import time
from io import BytesIO

from confluent_kafka import Producer
from fastavro import parse_schema, schemaless_writer

from root.src.utils import AzureSchemaRegistry, KafkaConfig, logger, read_kafka_config, read_schema

from .api.ny_times import NYTimesAPI, fetch_books


def create_producer(kafka_config: KafkaConfig) -> Producer:
    """Create a Kafka producer.

    Args:
        kafka_config: The Kafka configuration to use.

    Returns:
        A Kafka producer.
    """
    config = read_kafka_config(kafka_config)
    return Producer(config)


def delivery_callback(err, msg):
    """Delivery callback for Kafka producer.

    Args:
        err: The error message.
        msg: The message.
    """
    if err:
        logger.error(f"Message failed delivery: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")


def produce_message(producer: Producer, topic: str, dict_message: dict) -> None:
    """Produce a message to Kafka.

    Args:
        producer: The Kafka producer.
        topic: The Kafka topic to send the message to.
        dict_message: The message to send.
    """
    avro_schema = read_schema("book_schema")

    schema = parse_schema(json.loads(avro_schema))

    fo = BytesIO()
    schemaless_writer(fo, schema, dict_message)

    producer.produce(topic, value=fo.getvalue(), callback=delivery_callback)
    producer.flush()


def produce_books(nyapi: NYTimesAPI, selected_lists: list[str], kafka_config: KafkaConfig, topic: str) -> None:
    """Produce books to Kafka.

    Args:
        nyapi: The NYTimes API.
        selected_lists: The book lists to fetch.
        kafka_config: The Kafka configuration to use.
        topic: The Kafka topic to send the messages to.
    """
    producer = create_producer(kafka_config)
    AzureSchemaRegistry().register_schema("base_schema_group", "book_schema", read_schema("book_schema"))

    for book_list in selected_lists:
        time.sleep(1)  # To avoid rate limiting
        books = fetch_books(nyapi, book_list)

        logger.info(f"Producing {len(books)} messages to Kafka")
        for book in books:
            produce_message(producer, topic, book)
