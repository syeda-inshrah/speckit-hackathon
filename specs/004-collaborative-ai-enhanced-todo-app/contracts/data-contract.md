# Data Contract: Collaborative AI-Enhanced Todo Application

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
    },
    "aiFeatures": {
      "enablePredictions": "boolean",
      "enableRecommendations": "boolean",
      "enableSmartScheduling": "boolean"
    }
  },
  "productivityMetrics": {
    "averageCompletionRate": "float",
    "peakProductivityHours": "array of integers (hours)",
    "preferredWorkDays": "array of integers (days of week)"
  }
}
```

## Workspace Schema
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string (optional)",
  "ownerId": "uuid (foreign key to user)",
  "members": [
    {
      "userId": "uuid",
      "role": "admin|editor|viewer",
      "joinedAt": "ISO 8601 timestamp"
    }
  ],
  "settings": {
    "allowGuests": "boolean",
    "requireApproval": "boolean",
    "defaultPermissions": "string"
  },
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp"
}
```

## Todo Item Schema
```json
{
  "id": "uuid",
  "userId": "uuid (foreign key, null if team task)",
  "workspaceId": "uuid (foreign key, null if personal task)",
  "title": "string (max 255 chars)",
  "description": "string (max 1000 chars, optional)",
  "completed": "boolean (default: false)",
  "dueDate": "ISO 8601 timestamp (optional)",
  "priority": "low|medium|high (default: medium)",
  "aiPriorityScore": "float (0-1, optional)",
  "estimatedDuration": "integer (minutes, optional)",
  "assignedTo": "uuid (user id for team tasks)",
  "category": "string (optional)",
  "tags": "array of strings (max 10, max 30 chars each)",
  "collaborators": "array of uuids (user ids)",
  "comments": [
    {
      "id": "uuid",
      "userId": "uuid",
      "text": "string",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp"
    }
  ],
  "aiMetadata": {
    "predictedPriority": "float (0-1)",
    "estimatedDuration": "integer (minutes)",
    "categoryPrediction": "string",
    "createdWithNLP": "boolean",
    "confidenceScore": "float (0-1)"
  },
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp",
  "completedAt": "ISO 8601 timestamp (optional)",
  "lastActivityAt": "ISO 8601 timestamp"
}
```

## AI Training Data Schema
```json
{
  "id": "uuid",
  "userId": "uuid",
  "featureType": "priority_prediction|duration_estimation|categorization",
  "inputData": "object (anonymized feature vector)",
  "actualOutcome": "any (actual result for training)",
  "predictedOutcome": "any (prediction at time of event)",
  "accuracy": "float (0-1)",
  "feedbackProvided": "boolean (whether user corrected AI)",
  "feedbackValue": "any (corrected value if provided)",
  "collectedAt": "ISO 8601 timestamp",
  "processedForTraining": "boolean (flag for data pipeline)"
}
```

## Collaboration Activity Schema
```json
{
  "id": "uuid",
  "workspaceId": "uuid",
  "userId": "uuid",
  "action": "create_todo|update_todo|complete_todo|comment|assign|join_workspace|leave_workspace",
  "targetId": "uuid (affected entity id)",
  "targetType": "todo|workspace|comment",
  "metadata": "object (action-specific data)",
  "createdAt": "ISO 8601 timestamp"
}
```

## Indexes
- Users: email (unique), username (unique), createdAt
- Workspaces: ownerId, createdAt
- Todos: userId, workspaceId, completed, dueDate, createdAt, assignedTo
- Activities: workspaceId, userId, createdAt, targetType

## Data Validation Rules
- Email: RFC 5322 compliant
- Username: 3-30 alphanumeric chars + underscores/hyphens
- Title: 1-255 characters
- Description: 0-1000 characters
- Priority: Must be one of allowed values
- AI scores: Between 0 and 1
- Estimated duration: Positive integer
- Tags: Maximum 10 tags, each max 30 characters

## Privacy Requirements
- AI training data anonymized before processing
- Users can opt out of data collection for AI
- Right to deletion includes AI training data
- GDPR compliance for EU users
- Data minimization for AI features
- Consent tracking for AI feature usage

## Data Retention Policy
- Active user data: Indefinite while account exists
- AI training data: 2 years from collection
- Activity logs: 1 year
- Soft-deleted records: 30 days before hard deletion
- Temporary AI processing data: 1 hour

## Backup Strategy
- Daily backups of all user data
- Separate backup for AI model parameters
- Point-in-time recovery available for 7 days
- Encrypted backup storage
- Backup integrity verification