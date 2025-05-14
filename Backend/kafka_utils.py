"""
Kafka utilities for the backend service.
Contains helper functions for producing and consuming messages.
"""

import json
import os
import logging
from kafka import KafkaProducer, KafkaConsumer
from typing import Dict, Any, Generator, Optional, List

logger = logging.getLogger(__name__)

def get_kafka_producer() -> KafkaProducer:
    """
    Create and return a Kafka producer instance.
    
    Returns:
        KafkaProducer: Configured Kafka producer
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=os.environ.get('KAFKA_BROKER', 'kub-kafka:9092'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,   # Retry sending a few times
            linger_ms=5  # Small delay to batch messages
        )
        logger.info("Kafka producer created successfully")
        return producer
    except Exception as e:
        logger.error(f"Failed to create Kafka producer: {e}")
        raise

def send_message(topic: str, message: Dict[str, Any], key: Optional[str] = None) -> bool:
    """
    Send a message to a Kafka topic.
    
    Args:
        topic (str): Kafka topic to send message to
        message (Dict[str, Any]): Message payload
        key (Optional[str]): Message key for partitioning
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        producer = get_kafka_producer()
        
        # Convert key to bytes if provided
        key_bytes = key.encode('utf-8') if key else None
        
        # Send message
        future = producer.send(topic, value=message, key=key_bytes)
        
        # Block until message is sent (or timeout)
        record_metadata = future.get(timeout=10)
        
        logger.info(f"Message sent to topic {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")
        
        # Close producer
        producer.flush()
        producer.close()
        
        return True
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")
        return False

def get_consumer(topic: str, group_id: str = 'default-group', auto_offset_reset: str = 'earliest') -> KafkaConsumer:
    """
    Create and return a Kafka consumer instance.
    
    Args:
        topic (str): Kafka topic to consume from
        group_id (str): Consumer group ID
        auto_offset_reset (str): Where to start reading messages ('earliest' or 'latest')
    
    Returns:
        KafkaConsumer: Configured Kafka consumer
    """
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=os.environ.get('KAFKA_BROKER', 'kub-kafka:9092'),
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.info(f"Created Kafka consumer for topic {topic}, group {group_id}")
        return consumer
    except Exception as e:
        logger.error(f"Failed to create Kafka consumer: {e}")
        raise

def consume_messages(topic: str, group_id: str = 'default-group') -> Generator[Dict[str, Any], None, None]:
    """
    Generator function to consume messages from a Kafka topic.
    
    Args:
        topic (str): Kafka topic to consume from
        group_id (str): Consumer group ID
    
    Yields:
        Dict[str, Any]: Message payload
    """
    consumer = get_consumer(topic, group_id)
    try:
        for message in consumer:
            logger.info(f"Received message from topic {message.topic}, partition {message.partition}, offset {message.offset}")
            yield message.value
    finally:
        consumer.close()

def list_topics() -> List[str]:
    """
    List all available Kafka topics.
    
    Returns:
        List[str]: List of topic names
    """
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=os.environ.get('KAFKA_BROKER', 'kub-kafka:9092')
        )
        topics = consumer.topics()
        consumer.close()
        return list(topics)
    except Exception as e:
        logger.error(f"Failed to list Kafka topics: {e}")
        return [] 