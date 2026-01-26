# API Contract: Mobile-Responsive Todo Application

## Base URL
```
https://api.mobiletodoapp.com/v1
```

## Authentication
All endpoints require authentication via JWT token in Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Common Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2023-07-15T10:30:00Z"
}
```

## Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  },
  "timestamp": "2023-07-15T10:30:00Z"
}
```

## Endpoints

### User Management
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile

### Todo Items
- `GET /todos` - Get user's todos with pagination
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo
- `PATCH /todos/{id}/complete` - Toggle completion status

### Mobile-Specific Endpoints
- `POST /todos/{id}/photo` - Upload photo attachment
- `GET /todos/offline-sync` - Sync offline changes
- `GET /todos/nearby` - Get location-based todos (requires location)

## Rate Limiting
- Authenticated requests: 1000/hour
- Unauthenticated requests: 100/hour
- File uploads: 10/hour

## Request Size Limits
- JSON payloads: 1MB
- Photo uploads: 5MB
- Batch operations: 100 items max

## Response Time SLAs
- 95th percentile: < 500ms
- 99th percentile: < 1000ms
- Mobile-optimized responses: < 300ms for critical paths