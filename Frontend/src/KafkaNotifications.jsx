import { useState, useEffect } from 'react';
import './KafkaNotifications.css';

const KafkaNotifications = ({ notificationsEnabled = true }) => {
  const [notifications, setNotifications] = useState([]);
  const [polling, setPolling] = useState(false);

  // Poll for Kafka events
  useEffect(() => {
    if (!notificationsEnabled) return;

    const pollInterval = setInterval(() => {
      fetchKafkaEvents();
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(pollInterval);
  }, [notificationsEnabled]);

  // Fetch Kafka events
  const fetchKafkaEvents = async () => {
    try {
      const response = await fetch('/api/kafka/events');
      if (response.ok) {
        const data = await response.json();
        if (data.events && data.events.length > 0) {
          // Add new events to notifications
          setNotifications(prev => [
            ...data.events.map(event => ({
              id: `${event.timestamp}-${Math.random()}`,
              timestamp: new Date(event.timestamp),
              type: event.event_type,
              message: getEventMessage(event),
              read: false
            })),
            ...prev
          ].slice(0, 10)); // Keep only the 10 most recent notifications
        }
      }
    } catch (error) {
      console.error("Error fetching Kafka events:", error);
    }
  };

  // Convert event to readable message
  const getEventMessage = (event) => {
    switch (event.event_type) {
      case 'user_created':
        return `New user registered: ${event.email}`;
      case 'user_details_created':
        return `User profile completed: ${event.name}`;
      default:
        return `Event: ${event.event_type}`;
    }
  };

  // Mark notification as read
  const markAsRead = (id) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === id 
          ? { ...notification, read: true } 
          : notification
      )
    );
  };

  // Remove notification
  const removeNotification = (id) => {
    setNotifications(prev => 
      prev.filter(notification => notification.id !== id)
    );
  };

  // Format timestamp
  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Demo: simulate a new event (for testing without backend)
  const simulateEvent = () => {
    const eventTypes = ['user_created', 'user_details_created'];
    const randomType = eventTypes[Math.floor(Math.random() * eventTypes.length)];
    
    const event = {
      event_type: randomType,
      email: randomType === 'user_created' ? 'user@example.com' : undefined,
      name: randomType === 'user_details_created' ? 'John Doe' : undefined,
      timestamp: new Date().toISOString()
    };
    
    setNotifications(prev => [
      {
        id: `${event.timestamp}-${Math.random()}`,
        timestamp: new Date(),
        type: event.event_type,
        message: getEventMessage(event),
        read: false
      },
      ...prev
    ].slice(0, 10));
  };

  return (
    <div className="kafka-notifications-container">
      <div className="kafka-notifications-header">
        <h3>Kafka Event Stream</h3>
        <div className="notification-controls">
          <button onClick={simulateEvent} className="simulate-btn">
            Simulate Event
          </button>
          <div className={`status-indicator ${polling ? 'active' : 'inactive'}`}>
            {polling ? 'Streaming' : 'Paused'}
          </div>
        </div>
      </div>
      
      <div className="notifications-list">
        {notifications.length === 0 ? (
          <div className="no-notifications">No events received yet</div>
        ) : (
          notifications.map(notification => (
            <div 
              key={notification.id} 
              className={`notification-item ${notification.read ? 'read' : 'unread'}`}
              onClick={() => markAsRead(notification.id)}
            >
              <div className="notification-time">{formatTime(notification.timestamp)}</div>
              <div className="notification-type">{notification.type}</div>
              <div className="notification-message">{notification.message}</div>
              <button 
                className="close-notification" 
                onClick={(e) => {
                  e.stopPropagation();
                  removeNotification(notification.id);
                }}
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
      
      <div className="kafka-footer">
        <button 
          className={`stream-toggle ${polling ? 'active' : 'inactive'}`}
          onClick={() => setPolling(!polling)}
        >
          {polling ? 'Pause Stream' : 'Start Stream'}
        </button>
        {notifications.length > 0 && (
          <button 
            className="clear-all"
            onClick={() => setNotifications([])}
          >
            Clear All
          </button>
        )}
      </div>
    </div>
  );
};

export default KafkaNotifications; 