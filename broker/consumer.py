from confluent_kafka import Consumer

import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_messages(topic: str, group_id: str):
    consumer_conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
    }
    
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    logger.info(f"consumer assignes: {consumer.assignment()}")
    
    messages = []
    try:
        while True:

            msg = consumer.poll(1)

            if msg is None:
                if consumer.assignment() != []: 
                    logger.info(f"Recieved {len(messages)} messages")
                    logger.info(f"Finished consuming messages from topic '{topic}'.")
                    break
                else:
                    logger.info("Waiting for assignment...")
                continue

            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue  

            message = json.loads(msg.value().decode('utf-8'))
            messages.append(message)
    
    except Exception as e:
        logger.error(f"Exception: {e}")

    finally:
        consumer.close()

    return messages