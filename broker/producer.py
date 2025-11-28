from confluent_kafka import Producer

import json


def raport_delivery(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce(message: dict, topic: str):
    producer = Producer(
        {"bootstrap.servers": "kafka:9092"}
    )
    
    encoded_message = json.dumps(message).encode("utf-8")

    producer.produce(
        topic, 
        encoded_message,
        callback=raport_delivery
    )
    producer.flush()