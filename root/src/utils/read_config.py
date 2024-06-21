import importlib.resources as ir
import json
import os
import pathlib
from enum import Enum

from root import resources

__all__ = ["read_kafka_config", "KafkaConfig", "read_schema"]


class KafkaConfig(Enum):
    DEV = "kafka_config.json"
    DEV_LOCAL = "kafka_config_dev.json"


def read_kafka_config(kafka_config: KafkaConfig) -> dict:
    """Read the Kafka configuration from a file.

    Args:
        kafka_config: The Kafka configuration to read.

    Returns:
        The Kafka configuration.
    """
    files = str(ir.files(resources))
    with open(pathlib.Path(files, kafka_config.value)) as f:
        data = json.load(f)
    kafka_sasl_password = os.environ.get("KAFKA_SASL_PASSWORD")

    if kafka_sasl_password is None:
        raise ValueError("KAFKA_SASL_PASSWORD environment variable not set")

    data["sasl.password"] = kafka_sasl_password
    return data


def read_schema(schema_name: str) -> str:
    """Read an Avro schema from a file.

    Args:
        schema_name: The name of the schema to read.

    Returns:
        The Avro schema.
    """
    files = str(ir.files(resources))
    with open(pathlib.Path(files, schema_name + ".avsc")) as f:
        data = f.read()
    return data
