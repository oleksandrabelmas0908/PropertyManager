import os
import logging
from confluent_kafka.admin import AdminClient, NewTopic


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_startup(retries: int = 3, retry_delay: int = 2):
    """Create a `test_topic` in Kafka if it does not already exist.

    This function is safe to call multiple times. It uses the Confluent
    AdminClient to create the topic and tolerates the topic already
    existing.
    """
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

    topics = [
        NewTopic(topic="match_topic", num_partitions=1, replication_factor=1),
        NewTopic(topic="proceeded_match_topic", num_partitions=1, replication_factor=1),
        NewTopic(topic="send_to_parse_topic", num_partitions=1, replication_factor=1),
        NewTopic(topic="parsed_data_topic", num_partitions=1, replication_factor=1),
    ]

    for attempt in range(1, retries + 1):
        try:
            admin = AdminClient({"bootstrap.servers": bootstrap})
            fs = admin.create_topics(topics, validate_only=False)

            # wait for results
            for t, f in fs.items():
                try:
                    f.result(timeout=10)
                    logger.info("Topic '%s' created or already exists", t)
                except Exception as exc:
                    # TOPIC_ALREADY_EXISTS will be raised as an exception; tolerate it
                    if "TOPIC_ALREADY_EXISTS" in str(exc) or "already exists" in str(exc):
                        logger.info("Topic '%s' already exists", t)
                    else:
                        logger.warning("Topic '%s' creation returned error: %s", t, exc)
            return True

        except Exception as e:
            logger.exception("Failed to create topic on attempt %d: %s", attempt, e)
            if attempt < retries:
                import time

                time.sleep(retry_delay)
            else:
                return False