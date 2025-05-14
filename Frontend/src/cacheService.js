/**
 * Frontend Cache Service
 * 
 * This service provides browser-side caching to improve performance and 
 * reduce API calls. It uses localStorage with expiration for simplicity.
 */

// Cache configuration
const CACHE_PREFIX = 'kub_cache_';
const DEFAULT_EXPIRY = 5 * 60 * 1000; // 5 minutes in milliseconds

/**
 * Set data in cache with expiration
 * @param {string} key - Cache key
 * @param {any} value - Value to cache
 * @param {number} expiry - Expiry time in milliseconds
 */
export function setCache(key, value, expiry = DEFAULT_EXPIRY) {
  if (!key) return false;
  
  try {
    const cacheItem = {
      value,
      expiry: Date.now() + expiry,
    };
    
    localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(cacheItem));
    return true;
  } catch (error) {
    console.error('Cache error:', error);
    return false;
  }
}

/**
 * Get data from cache
 * @param {string} key - Cache key
 * @returns {any|null} - Cached value or null if not found/expired
 */
export function getCache(key) {
  if (!key) return null;
  
  try {
    const cacheItemStr = localStorage.getItem(CACHE_PREFIX + key);
    if (!cacheItemStr) return null;
    
    const cacheItem = JSON.parse(cacheItemStr);
    
    // Check if expired
    if (cacheItem.expiry < Date.now()) {
      localStorage.removeItem(CACHE_PREFIX + key);
      return null;
    }
    
    return cacheItem.value;
  } catch (error) {
    console.error('Cache error:', error);
    return null;
  }
}

/**
 * Remove data from cache
 * @param {string} key - Cache key
 */
export function removeCache(key) {
  if (!key) return false;
  
  try {
    localStorage.removeItem(CACHE_PREFIX + key);
    return true;
  } catch (error) {
    console.error('Cache error:', error);
    return false;
  }
}

/**
 * Clear all cache data
 */
export function clearCache() {
  try {
    const keysToRemove = [];
    
    // Collect all cache keys
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(CACHE_PREFIX)) {
        keysToRemove.push(key);
      }
    }
    
    // Remove all cache keys
    keysToRemove.forEach(key => localStorage.removeItem(key));
    
    return true;
  } catch (error) {
    console.error('Cache error:', error);
    return false;
  }
}

/**
 * Clear expired cache entries
 */
export function cleanCache() {
  try {
    const now = Date.now();
    const keysToRemove = [];
    
    // Collect expired cache keys
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(CACHE_PREFIX)) {
        try {
          const cacheItemStr = localStorage.getItem(key);
          const cacheItem = JSON.parse(cacheItemStr);
          
          if (cacheItem.expiry < now) {
            keysToRemove.push(key);
          }
        } catch (e) {
          // If we can't parse it, remove it
          keysToRemove.push(key);
        }
      }
    }
    
    // Remove expired cache keys
    keysToRemove.forEach(key => localStorage.removeItem(key));
    
    return true;
  } catch (error) {
    console.error('Cache error:', error);
    return false;
  }
} 