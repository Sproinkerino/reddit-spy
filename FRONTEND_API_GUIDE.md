# Frontend API Integration Guide

This guide explains how to integrate the Reddit Stalker API with your React frontend application.

## API Base URL

```
http://localhost:8000  (Development)
https://reddit-spy.onrender.com/ (Production)
```

## Authentication

No authentication required for this API. Simply make HTTP requests to the endpoints.

## Available Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Reddit Stalker API is running",
  "status": "healthy"
}
```

### 2. Analyze Reddit User
Analyze a Reddit user and get an AI-generated summary.

**Endpoint:** `POST /analyze`

## Request Format

### Headers
```javascript
{
  "Content-Type": "application/json"
}
```

### Request Body
```javascript
{
  "user_id": "string",           // Your frontend user ID
  "user_to_search": "string",    // Reddit username to analyze
  "parameters": {                // Optional configuration
    "post_limit": 10,            // Number of posts to fetch (default: 10)
    "comment_limit": 100,        // Number of comments to fetch (default: 100)
    "model": "gpt-3.5-turbo",   // OpenAI model (default: "gpt-4o")
    "temperature": 0.5,          // AI creativity 0-1 (default: 0.5)
    "custom_prompt": "string"    // Custom analysis prompt
  }
}
```

## Response Format

### Success Response (200)
```javascript
{
  "success": true,
  "user_id": "frontend_user_123",
  "analyzed_user": "reddit_username",
  "summary": "AI-generated analysis of the user...",
  "error": null
}
```

### Error Responses

#### 400 Bad Request
```javascript
{
  "detail": "Error fetching data from Reddit: received 404 HTTP response"
}
```

#### 422 Validation Error
```javascript
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "user_to_search"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

#### 500 Internal Server Error
```javascript
{
  "detail": "Error communicating with OpenAI API: ..."
}
```

## React Integration Examples

### Basic Usage with Fetch

```javascript
const analyzeRedditUser = async (redditUsername, userId) => {
  try {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        user_to_search: redditUsername,
        parameters: {
          post_limit: 10,
          comment_limit: 50
        }
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing user:', error);
    throw error;
  }
};

// Usage
const handleAnalyze = async () => {
  try {
    const result = await analyzeRedditUser('spez', 'user123');
    console.log('Analysis:', result.summary);
  } catch (error) {
    console.error('Failed to analyze user:', error);
  }
};
```

### Using Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  }
});

const analyzeRedditUser = async (redditUsername, userId, options = {}) => {
  try {
    const response = await api.post('/analyze', {
      user_id: userId,
      user_to_search: redditUsername,
      parameters: {
        post_limit: options.postLimit || 10,
        comment_limit: options.commentLimit || 100,
        model: options.model || 'gpt-3.5-turbo',
        temperature: options.temperature || 0.5,
        ...options.customPrompt && { custom_prompt: options.customPrompt }
      }
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.detail);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error - please check your connection');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
};
```

### React Hook Example

```javascript
import { useState, useCallback } from 'react';

const useRedditAnalyzer = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const analyzeUser = useCallback(async (redditUsername, userId, options = {}) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          user_to_search: redditUsername,
          parameters: {
            post_limit: options.postLimit || 10,
            comment_limit: options.commentLimit || 100,
            model: options.model || 'gpt-3.5-turbo',
            temperature: options.temperature || 0.5,
            ...options.customPrompt && { custom_prompt: options.customPrompt }
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { analyzeUser, loading, error, result };
};

// Usage in component
const RedditAnalyzer = () => {
  const { analyzeUser, loading, error, result } = useRedditAnalyzer();
  const [username, setUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await analyzeUser(username, 'current_user_id');
    } catch (err) {
      // Error is already handled by the hook
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter Reddit username"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze User'}
        </button>
      </form>

      {error && <div className="error">Error: {error}</div>}
      
      {result && (
        <div className="result">
          <h3>Analysis for u/{result.analyzed_user}</h3>
          <p>{result.summary}</p>
        </div>
      )}
    </div>
  );
};
```

## Error Handling Best Practices

### 1. Network Errors
```javascript
try {
  const result = await analyzeRedditUser('username', 'user123');
} catch (error) {
  if (error.message.includes('Network error')) {
    // Show "Please check your internet connection" message
  } else if (error.message.includes('404')) {
    // Show "Reddit user not found" message
  } else {
    // Show generic error message
  }
}
```

### 2. Validation Errors
```javascript
try {
  const result = await analyzeRedditUser('', 'user123'); // Empty username
} catch (error) {
  if (error.message.includes('Field required')) {
    // Show "Please enter a valid Reddit username" message
  }
}
```

### 3. Rate Limiting
The API doesn't implement rate limiting, but you should implement client-side throttling to avoid overwhelming the server.

```javascript
const throttle = (func, delay) => {
  let timeoutId;
  let lastExecTime = 0;
  return function (...args) {
    const currentTime = Date.now();
    
    if (currentTime - lastExecTime > delay) {
      func.apply(this, args);
      lastExecTime = currentTime;
    } else {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
        lastExecTime = Date.now();
      }, delay - (currentTime - lastExecTime));
    }
  };
};

const throttledAnalyze = throttle(analyzeRedditUser, 2000); // 2 second throttle
```

## Environment Configuration

### Development
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### Production
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.onrender.com';
```

## Testing the API

You can test the API using the interactive documentation at:
- Development: `http://localhost:8000/docs`
- Production: `https://your-app.onrender.com/docs`

## Common Issues

1. **CORS Errors**: Make sure your frontend domain is allowed in the API's CORS settings
2. **Network Timeouts**: The API can take 10-30 seconds for complex analyses
3. **Invalid Usernames**: Always validate Reddit usernames before sending requests
4. **Rate Limiting**: Implement client-side throttling to avoid overwhelming the server

## Support

For API issues, check the server logs or contact the backend team.
