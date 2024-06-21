import argparse
import logging

from root.src.api.ny_times import NYTimesAPI
from root.src.producer import KafkaConfig, produce_books


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="This program fetches data from the NYTimes API and sends it to a specified Kafka topic."
    )

    parser.add_argument("-t", "--topic", required=True, help="The Kafka topic to send the data to.")

    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    nyapi = NYTimesAPI()

    # produce_books(nyapi, [nyapi.lists[0]], KafkaConfig.DEV, args.topic)
    produce_books(nyapi, nyapi.lists, KafkaConfig.DEV, args.topic)
