#!/usr/bin/env python
"""
Kafka Consumer for User Events

This script runs as a standalone service to consume and process user events from Kafka.
It demonstrates how events would be processed by different services in a microservices architecture.
"""

import os
import time
import json
import logging
from datetime import datetime
import sys
import requests  # For sending events back to the API

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("events_consumer.log")
    ]
)
logger = logging.getLogger("user_events_consumer")

# Import Kafka utilities
import kafka_utils

# Topic and consumer group
USER_EVENTS_TOPIC = "user_events"
CONSUMER_GROUP = "user-events-processor"

# API endpoint to report processed events
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def handle_user_created(event_data):
    """
    Handle user_created events
    
    In a real application, this might:
    - Send a welcome email
    - Create user in analytics system
    - Provision resources for the user
    """
    user_id = event_data.get("user_id")
    email = event_data.get("email")
    timestamp = event_data.get("timestamp")
    
    logger.info(f"Processing user_created event for user {user_id} ({email}) from {timestamp}")
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Example: Send welcome email (simulated)
    logger.info(f"📧 Welcome email sent to {email}")
    
    # Example: Creating analytics profile (simulated)
    logger.info(f"📊 Analytics profile created for user {user_id}")
    
    # Example: Log audit record (simulated)
    logger.info(f"📝 Audit log entry created for new user {user_id}")
    
    # Add processing result to the event data
    event_data["processing_result"] = {
        "welcome_email_sent": True,
        "analytics_profile_created": True,
        "audit_log_created": True,
        "processed_at": datetime.now().isoformat()
    }
    
    # Report the processed event
    report_processed_event(event_data)

def handle_user_details_created(event_data):
    """
    Handle user_details_created events
    
    In a real application, this might:
    - Update user profile in other systems
    - Send notifications
    - Generate reports
    """
    user_id = event_data.get("user_id")
    name = event_data.get("name")
    email = event_data.get("email")
    phone = event_data.get("phone")
    
    logger.info(f"Processing user_details_created event for user {user_id} ({name})")
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Example: Update user profile in CRM (simulated)
    logger.info(f"👤 CRM profile updated for {name} (ID: {user_id})")
    
    # Example: Send profile completion notification (simulated)
    logger.info(f"🔔 Profile completion notification sent to {email}")
    
    # Add processing result to the event data
    event_data["processing_result"] = {
        "crm_profile_updated": True,
        "notification_sent": True,
        "processed_at": datetime.now().isoformat()
    }
    
    # Report the processed event
    report_processed_event(event_data)

def report_processed_event(event_data):
    """Report the processed event back to the API for frontend display"""
    try:
        # Create a new event to show processing result
        processed_event = {
            "event_type": f"{event_data['event_type']}_processed",
            "original_event": event_data["event_type"],
            "user_id": event_data.get("user_id"),
            "email": event_data.get("email"),
            "name": event_data.get("name", ""),
            "processing_result": event_data.get("processing_result", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        # Try to send the processed event to the API
        try:
            response = requests.post(
                f"{API_BASE_URL}/kafka/publish/{USER_EVENTS_TOPIC}",
                json=processed_event,
                timeout=3
            )
            if response.status_code == 200:
                logger.info(f"Reported processed event to API: {processed_event['event_type']}")
            else:
                logger.warning(f"Failed to report processed event: {response.status_code} {response.text}")
        except Exception as e:
            logger.error(f"Error reporting processed event to API: {e}")
            
            # Fallback: Send directly to Kafka
            try:
                kafka_utils.send_message(
                    topic=USER_EVENTS_TOPIC,
                    message=processed_event
                )
                logger.info(f"Sent processed event directly to Kafka: {processed_event['event_type']}")
            except Exception as kafka_err:
                logger.error(f"Error sending processed event to Kafka: {kafka_err}")
    except Exception as e:
        logger.error(f"Error preparing processed event: {e}")

def process_event(event_data):
    """Process an event based on its type"""
    event_type = event_data.get("event_type")
    
    if event_type == "user_created":
        handle_user_created(event_data)
    elif event_type == "user_details_created":
        handle_user_details_created(event_data)
    else:
        logger.warning(f"Unknown event type: {event_type}")

def main():
    """Main consumer loop"""
    logger.info(f"Starting user events consumer (group: {CONSUMER_GROUP})")
    logger.info(f"Listening for events on topic: {USER_EVENTS_TOPIC}")
    logger.info(f"API base URL: {API_BASE_URL}")
    
    try:
        # Check if topic exists, create it if it doesn't
        topics = kafka_utils.list_topics()
        if USER_EVENTS_TOPIC not in topics:
            logger.info(f"Topic {USER_EVENTS_TOPIC} doesn't exist. It will be created when the first message is sent.")
        
        # Consume messages
        for event_data in kafka_utils.consume_messages(USER_EVENTS_TOPIC, CONSUMER_GROUP):
            try:
                logger.info(f"Received event: {json.dumps(event_data)[:100]}...")
                
                # Skip already processed events (to avoid loops)
                if event_data.get("event_type", "").endswith("_processed"):
                    logger.info(f"Skipping already processed event: {event_data.get('event_type')}")
                    continue
                    
                process_event(event_data)
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    except KeyboardInterrupt:
        logger.info("Consumer shutting down...")
    except Exception as e:
        logger.error(f"Consumer error: {e}")

if __name__ == "__main__":
    # Delay startup to ensure Kafka is ready
    time.sleep(5)
    main() 