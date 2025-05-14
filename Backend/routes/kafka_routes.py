"""
Kafka API routes for sending and receiving messages.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

import kafka_utils
from auth import get_current_user

router = APIRouter(
    prefix="/kafka",
    tags=["kafka"],
    responses={404: {"description": "Not found"}},
)

class Message(BaseModel):
    topic: str
    message: Dict[str, Any]
    key: Optional[str] = None
    
class Topic(BaseModel):
    name: str
    partitions: int = 1
    replication_factor: int = 1

@router.get("/topics")
async def get_topics(current_user = Depends(get_current_user)):
    """
    Get a list of all Kafka topics.
    """
    try:
        topics = kafka_utils.list_topics()
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topics: {str(e)}")

@router.post("/send")
async def send_message(message_data: Message, current_user = Depends(get_current_user)):
    """
    Send a message to a Kafka topic.
    """
    try:
        # Add user info to message metadata
        if isinstance(message_data.message, dict):
            message_data.message.setdefault("metadata", {})
            message_data.message["metadata"]["user_id"] = current_user.id
        
        success = kafka_utils.send_message(
            topic=message_data.topic, 
            message=message_data.message,
            key=message_data.key
        )
        
        if success:
            return {"status": "success", "message": "Message sent to Kafka topic"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send message")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@router.get("/healthcheck")
async def kafka_health():
    """
    Check if Kafka is available and functioning.
    """
    try:
        topics = kafka_utils.list_topics()
        return {
            "status": "healthy", 
            "broker": "connected",
            "topics_count": len(topics)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Kafka unhealthy: {str(e)}")

# For testing purposes - you might want to remove this in production
@router.post("/test-producer")
async def test_produce(topic: str = "test-topic", message: str = "Hello Kafka"):
    """
    Test endpoint to produce a message to Kafka.
    """
    try:
        test_message = {
            "content": message,
            "source": "api-test"
        }
        
        success = kafka_utils.send_message(topic, test_message)
        
        if success:
            return {"status": "success", "message": f"Test message sent to {topic}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send test message")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in test producer: {str(e)}") 