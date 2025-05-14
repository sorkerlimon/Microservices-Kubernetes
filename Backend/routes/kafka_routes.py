"""
Kafka API routes for testing and monitoring Kafka functionality.
"""

from fastapi import APIRouter, BackgroundTasks
import subprocess
import os
import json
import logging
import kafka_utils
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/kafka",
    tags=["kafka"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for recent events (for demo purposes)
# In a production environment, you might use Redis or a database
recent_events = []
MAX_STORED_EVENTS = 50

@router.get("/topics")
async def list_kafka_topics() -> Dict[str, List[str]]:
    """
    List all available Kafka topics.
    """
    try:
        topics = kafka_utils.list_topics()
        return {"topics": topics}
    except Exception as e:
        logger.error(f"Error listing topics: {e}")
        return {"topics": [], "error": str(e)}

@router.post("/topics/{topic_name}")
async def create_topic(topic_name: str) -> Dict[str, Any]:
    """
    Create a new Kafka topic.
    """
    try:
        # In a real implementation, you would use the AdminClient
        # For simplicity, we'll just send a message to create the topic
        result = kafka_utils.send_message(
            topic=topic_name,
            message={"action": "create_topic", "timestamp": "now"}
        )
        if result:
            return {"status": "success", "message": f"Topic '{topic_name}' created"}
        else:
            return {"status": "error", "message": "Failed to create topic"}
    except Exception as e:
        logger.error(f"Error creating topic: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/publish/{topic_name}")
async def publish_message(topic_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Publish a message to a Kafka topic.
    """
    try:
        # Store message in recent events for the UI to fetch
        if topic_name == "user_events":
            # Add timestamp if not present
            if "timestamp" not in message:
                message["timestamp"] = datetime.now().isoformat()
            
            # Save to in-memory storage for the /events API
            recent_events.append(message)
            # Keep only the most recent events
            if len(recent_events) > MAX_STORED_EVENTS:
                recent_events.pop(0)
        
        result = kafka_utils.send_message(topic=topic_name, message=message)
        if result:
            return {"status": "success", "message": "Message published successfully"}
        else:
            return {"status": "error", "message": "Failed to publish message"}
    except Exception as e:
        logger.error(f"Error publishing message: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/events")
async def get_recent_events(since: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get recent Kafka events for the notification UI.
    Optionally filter by timestamp with 'since' parameter.
    """
    try:
        # If since parameter provided, filter events
        if since:
            try:
                since_dt = datetime.fromisoformat(since)
                filtered_events = [
                    event for event in recent_events 
                    if datetime.fromisoformat(event.get("timestamp", "")) > since_dt
                ]
                return {"events": filtered_events}
            except (ValueError, TypeError):
                # If invalid timestamp format, ignore the filter
                pass
        
        # Return all recent events
        return {"events": recent_events}
    except Exception as e:
        logger.error(f"Error retrieving events: {e}")
        return {"events": [], "error": str(e)}

@router.post("/start-consumer")
async def start_consumer(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Start the user events consumer in the background.
    """
    def run_consumer():
        try:
            # Use Popen to run the consumer as a background process
            process = subprocess.Popen(
                ["python", "user_events_consumer.py"], 
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Log standard output in a separate thread
            def log_output():
                for line in process.stdout:
                    logger.info(f"Consumer output: {line.decode().strip()}")
                for line in process.stderr:
                    logger.error(f"Consumer error: {line.decode().strip()}")
            
            import threading
            threading.Thread(target=log_output, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error starting consumer: {e}")
    
    background_tasks.add_task(run_consumer)
    return {"status": "success", "message": "Consumer started in background"}

@router.get("/status")
async def kafka_status() -> Dict[str, Any]:
    """
    Get Kafka status including topics and broker information.
    """
    try:
        topics = kafka_utils.list_topics()
        
        # For a simple check, just try to send a test message
        broker_status = "healthy"
        try:
            kafka_utils.send_message("kafka_health_check", {"check": "ping"})
        except Exception as e:
            broker_status = f"unhealthy: {str(e)}"
        
        return {
            "status": "healthy" if broker_status == "healthy" else "unhealthy",
            "broker": broker_status,
            "topics_count": len(topics),
            "topics": topics
        }
    except Exception as e:
        logger.error(f"Error checking Kafka status: {e}")
        return {"status": "error", "message": str(e)} 