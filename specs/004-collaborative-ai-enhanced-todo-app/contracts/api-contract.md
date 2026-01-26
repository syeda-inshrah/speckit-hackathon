# API Contract: Collaborative AI-Enhanced Todo Application

## Base URL
```
https://api.ai.todoapp.com/v1
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
  "timestamp": "2023-07-15T10:30:00Z",
  "requestId": "uuid"
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
  "timestamp": "2023-07-15T10:30:00Z",
  "requestId": "uuid"
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

### AI-Powered Endpoints
- `POST /ai/predict-priority` - Get AI priority prediction for a task
- `POST /ai/estimate-duration` - Get AI duration estimate for a task
- `GET /ai/recommendations` - Get AI-powered task recommendations
- `POST /ai/parse-task` - Parse natural language task description
- `GET /ai/insights/productivity` - Get productivity insights
- `GET /ai/insights/suggestions` - Get AI suggestions

### Collaboration Endpoints
- `GET /workspaces` - Get user's workspaces
- `POST /workspaces` - Create new workspace
- `GET /workspaces/{id}` - Get specific workspace
- `PUT /workspaces/{id}` - Update workspace
- `DELETE /workspaces/{id}` - Delete workspace
- `POST /workspaces/{id}/invite` - Invite member to workspace
- `DELETE /workspaces/{id}/members/{memberId}` - Remove member
- `GET /workspaces/{id}/activity` - Get workspace activity feed
- `POST /workspaces/{id}/todos` - Create team todo
- `PUT /workspaces/{id}/todos/{todoId}` - Update team todo
- `POST /workspaces/{id}/todos/{todoId}/assign` - Assign team todo

### Real-time Endpoints
- `GET /ws` - WebSocket connection for real-time updates
- `POST /realtime/sync` - Manual sync request

## Rate Limiting
- Authenticated requests: 1000/hour
- AI requests: 100/hour per user
- Unauthenticated requests: 100/hour
- File uploads: 10/hour

## Request Size Limits
- JSON payloads: 1MB
- Natural language processing: 500 characters
- Batch operations: 50 items max

## Response Time SLAs
- Standard API: 95th percentile < 500ms
- AI predictions: 95th percentile < 200ms
- Real-time updates: < 1000ms
- Collaboration sync: < 500ms