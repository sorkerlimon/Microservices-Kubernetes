// API service for backend communication
import { getCache, setCache, removeCache } from './cacheService';

const API_URL = 'http://localhost:8000';

// Cache expiry times (in milliseconds)
const CACHE_TIMES = {
  SHORT: 2 * 60 * 1000, // 2 minutes
  MEDIUM: 10 * 60 * 1000, // 10 minutes
  LONG: 30 * 60 * 1000 // 30 minutes
};

// User Authentication
export async function loginUser(email, password) {
  try {
    // Login should always go to server, not cached
    const response = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Login failed');
    }
    
    const userData = await response.json();
    
    // Cache user data on successful login
    setCache(`user:${userData.id}`, userData, CACHE_TIMES.MEDIUM);
    
    return userData;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
}

// User Registration
export async function registerUser(userData) {
  try {
    // Registration should always go to server, not cached
    // Step 1: Create the user account
    const userResponse = await fetch(`${API_URL}/users/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
      }),
    });
    
    if (!userResponse.ok) {
      const errorData = await userResponse.json();
      throw new Error(errorData.detail || 'Failed to create user');
    }
    
    const newUser = await userResponse.json();
    
    // Step 2: Add user details
    const detailsResponse = await fetch(`${API_URL}/users/${newUser.id}/details/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: userData.name,
        email: userData.email,
        phone: userData.phone,
      }),
    });
    
    if (!detailsResponse.ok) {
      const errorData = await detailsResponse.json();
      throw new Error(errorData.detail || 'Failed to add user details');
    }
    
    // Get the complete user with details
    const completeUser = await getUserById(newUser.id);
    
    return completeUser;
  } catch (error) {
    console.error('Registration failed:', error);
    throw error;
  }
}

// Get user by ID
export async function getUserById(userId) {
  try {
    // Check cache first
    const cacheKey = `user:${userId}`;
    const cachedUser = getCache(cacheKey);
    
    if (cachedUser) {
      return cachedUser;
    }
    
    // If not in cache, fetch from API
    const response = await fetch(`${API_URL}/users/${userId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch user data');
    }
    
    const userData = await response.json();
    
    // Cache the user data
    setCache(cacheKey, userData, CACHE_TIMES.MEDIUM);
    
    return userData;
  } catch (error) {
    console.error(`Failed to fetch user ${userId}:`, error);
    throw error;
  }
}

// Get all users
export async function getAllUsers() {
  try {
    // Check cache first
    const cacheKey = 'users:all';
    const cachedUsers = getCache(cacheKey);
    
    if (cachedUsers) {
      return cachedUsers;
    }
    
    // If not in cache, fetch from API
    const response = await fetch(`${API_URL}/users/`);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    
    const users = await response.json();
    
    // For each user, fetch their details
    const usersWithDetails = await Promise.all(
      users.map(async (user) => {
        try {
          return await getUserById(user.id);
        } catch (error) {
          return user; // Return just the user if details can't be fetched
        }
      })
    );
    
    // Cache the full user list
    setCache(cacheKey, usersWithDetails, CACHE_TIMES.SHORT);
    
    return usersWithDetails;
  } catch (error) {
    console.error('Failed to fetch users:', error);
    throw error;
  }
}

// Logout user
export function logoutUser() {
  // Clear any user-specific cache on logout
  removeCache('users:all');
  return true;
}

// Kafka API endpoints
export const getKafkaTopics = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) throw new Error('Not authenticated');
    
    const response = await fetch(`${API_URL}/kafka/topics`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch Kafka topics: ${response.status}`);
    }
    
    const data = await response.json();
    return data.topics;
  } catch (error) {
    console.error('Error fetching Kafka topics:', error);
    throw error;
  }
};

export const sendKafkaMessage = async (topic, message, key = null) => {
  try {
    const token = localStorage.getItem('token');
    if (!token) throw new Error('Not authenticated');
    
    const payload = {
      topic,
      message,
      key
    };
    
    const response = await fetch(`${API_URL}/kafka/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error(`Failed to send Kafka message: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error sending Kafka message:', error);
    throw error;
  }
};

export const checkKafkaHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/kafka/healthcheck`);
    
    if (!response.ok) {
      throw new Error(`Kafka health check failed: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Kafka health check error:', error);
    return {
      status: 'unhealthy',
      error: error.message
    };
  }
};

export const sendTestMessage = async (topic = 'test-topic', message = 'Hello from frontend') => {
  try {
    const response = await fetch(`${API_URL}/kafka/test-producer?topic=${encodeURIComponent(topic)}&message=${encodeURIComponent(message)}`);
    
    if (!response.ok) {
      throw new Error(`Failed to send test message: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error sending test message:', error);
    throw error;
  }
}; 