# Data Contract: Mobile-Responsive Todo Application

## User Schema
```json
{
  "id": "uuid",
  "email": "string (unique, indexed)",
  "username": "string (unique, indexed)",
  "firstName": "string",
  "lastName": "string",
  "avatar": "string (URL)",
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp",
  "lastActiveAt": "ISO 8601 timestamp",
  "preferences": {
    "theme": "light|dark|auto",
    "notifications": {
      "email": "boolean",
      "push": "boolean",
      "reminders": "boolean"
    }
  }
}
```

## Todo Item Schema
```json
{
  "id": "uuid",
  "userId": "uuid (foreign key)",
  "title": "string (max 255 chars)",
  "description": "string (max 1000 chars, optional)",
  "completed": "boolean (default: false)",
  "dueDate": "ISO 8601 timestamp (optional)",
  "priority": "low|medium|high (default: medium)",
  "category": "string (optional)",
  "location": {
    "lat": "float",
    "lng": "float",
    "radius": "integer (meters, optional)"
  },
  "attachments": [
    {
      "id": "uuid",
      "type": "image|document|other",
      "url": "string (URL)",
      "size": "integer (bytes)",
      "filename": "string",
      "uploadedAt": "ISO 8601 timestamp"
    }
  ],
  "tags": "array of strings (max 10, max 30 chars each)",
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp",
  "completedAt": "ISO 8601 timestamp (optional)"
}
```

## Offline Sync Schema
```json
{
  "id": "uuid",
  "userId": "uuid",
  "operation": "create|update|delete",
  "entityType": "todo|user|attachment",
  "entityId": "uuid",
  "payload": "object (the entity data)",
  "status": "pending|synced|failed",
  "attempts": "integer (default: 0)",
  "createdAt": "ISO 8601 timestamp",
  "syncedAt": "ISO 8601 timestamp (optional)"
}
```

## Indexes
- Users: email (unique), username (unique), createdAt
- Todos: userId, completed, dueDate, createdAt
- Attachments: todoId, createdAt

## Data Validation Rules
- Email: RFC 5322 compliant
- Username: 3-30 alphanumeric chars + underscores/hyphens
- Title: 1-255 characters
- Description: 0-1000 characters
- Priority: Must be one of allowed values
- Due date: Cannot be in the past (server-side validation)
- Tags: Maximum 10 tags, each max 30 characters

## Data Retention Policy
- Active user data: Indefinite while account exists
- Soft-deleted records: 30 days before hard deletion
- Failed sync attempts: 7 days
- Temporary upload data: 1 hour if not associated with todo

## Privacy Requirements
- Personal data encrypted at rest
- GDPR compliance for EU users
- Right to data portability
- Right to deletion
- Consent tracking for marketing communications

## Backup Strategy
- Daily backups of all user data
- Point-in-time recovery available for 7 days
- Encrypted backup storage
- Backup integrity verification

## Data Migration Requirements
- Zero downtime migrations
- Backward compatibility maintained during transition
- Rollback capability within 24 hours
- User data preserved during schema updates