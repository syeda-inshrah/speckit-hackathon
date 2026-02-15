# Phase 3 Testing Guide

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL database (Neon)
- Groq API key

### 1. Backend Setup

```bash
cd phase-3/backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add:
# - GROQ_API_KEY=your_groq_api_key
# - DATABASE_URL=your_neon_database_url
# - JWT_SECRET=your_secret_key

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

Backend should be running at: http://localhost:7860

### 2. Frontend Setup

```bash
cd phase-3/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running at: http://localhost:3000

## Testing the Application

### Step 1: Create an Account

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter your details:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
4. Click "Sign Up"

### Step 2: Sign In

1. Go to http://localhost:3000/signin
2. Enter your credentials
3. Click "Sign In"
4. You should be redirected to the dashboard

### Step 3: Test the Chat Interface

1. Click "Chat" in the navigation
2. You should see the chat interface

### Step 4: Test MCP Tools via Chat

#### Test 1: Add Task (add_task MCP tool)

**Input:**
```
Add a task to buy groceries
```

**Expected Output:**
```
✓ Created task: 'buy groceries'

What would you like to do next?
```

**What Happens:**
1. Groq analyzes intent → detects "create_task"
2. Extracts title: "buy groceries"
3. Calls MCP tool: `add_task(user_id, "buy groceries")`
4. Tool creates task in database
5. Groq generates natural language response

#### Test 2: List Tasks (list_tasks MCP tool)

**Input:**
```
Show me all my tasks
```

**Expected Output:**
```
Here are your tasks:

○ Task 1: buy groceries
```

**What Happens:**
1. Groq analyzes intent → detects "list_tasks"
2. Calls MCP tool: `list_tasks(user_id, completed=None)`
3. Tool retrieves tasks from database
4. Groq formats response with task list

#### Test 3: Add More Tasks

**Input:**
```
Add a task to finish the report
```

**Expected Output:**
```
✓ Created task: 'finish the report'

What would you like to do next?
```

**Input:**
```
Create a task to call the dentist
```

**Expected Output:**
```
✓ Created task: 'call the dentist'

What would you like to do next?
```

#### Test 4: Complete Task (complete_task MCP tool)

**Input:**
```
Mark task 1 as complete
```

**Expected Output:**
```
✓ Completed task: 'buy groceries'
```

**What Happens:**
1. Groq analyzes intent → detects "complete_task"
2. Extracts task_id: 1
3. Calls MCP tool: `complete_task(user_id, task_id=1)`
4. Tool marks task as completed in database
5. Groq confirms completion

#### Test 5: List Tasks Again

**Input:**
```
List my tasks
```

**Expected Output:**
```
Here are your tasks:

✓ Task 1: buy groceries
○ Task 2: finish the report
○ Task 3: call the dentist
```

Notice task 1 now has a checkmark (✓) indicating it's completed.

#### Test 6: Update Task (update_task MCP tool)

**Input:**
```
Update task 2 title to "Complete the quarterly report"
```

**Expected Output:**
```
✓ Updated task: 'Complete the quarterly report'
```

**What Happens:**
1. Groq analyzes intent → detects "update_task"
2. Extracts task_id: 2, new_title: "Complete the quarterly report"
3. Calls MCP tool: `update_task(user_id, task_id=2, title="Complete the quarterly report")`
4. Tool updates task in database
5. Groq confirms update

#### Test 7: Delete Task (delete_task MCP tool)

**Input:**
```
Delete task 3
```

**Expected Output:**
```
✓ Deleted task
```

**What Happens:**
1. Groq analyzes intent → detects "delete_task"
2. Extracts task_id: 3
3. Calls MCP tool: `delete_task(user_id, task_id=3)`
4. Tool deletes task from database
5. Groq confirms deletion

#### Test 8: Verify Deletion

**Input:**
```
Show my tasks
```

**Expected Output:**
```
Here are your tasks:

✓ Task 1: buy groceries
○ Task 2: Complete the quarterly report
```

Task 3 should no longer appear.

## Testing MCP Server Directly

You can test the MCP server independently of the chat interface:

### Option 1: Python Script

Create `test_mcp.py`:

```python
import asyncio
import json
from src.mcp_server.server import _add_task, _list_tasks, _complete_task
from src.core.database import get_session

async def test_mcp_tools():
    async for session in get_session():
        try:
            # Test user ID (replace with actual user ID from your database)
            user_id = "your-user-uuid-here"

            # Test add_task
            print("Testing add_task...")
            result = await _add_task(session, user_id, "Test Task", "Test Description")
            print(json.dumps(result, indent=2))

            # Test list_tasks
            print("\nTesting list_tasks...")
            result = await _list_tasks(session, user_id)
            print(json.dumps(result, indent=2))

        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
```

Run:
```bash
cd phase-3/backend
python test_mcp.py
```

### Option 2: Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todo-tasks": {
      "command": "python",
      "args": ["-m", "src.mcp_server.server"],
      "cwd": "D:\\hackathon-02\\phase-3\\backend",
      "env": {
        "DATABASE_URL": "your_database_url",
        "GROQ_API_KEY": "your_groq_api_key"
      }
    }
  }
}
```

Restart Claude Desktop and test the MCP tools directly.

## Debugging

### Check Backend Logs

The backend prints detailed logs:

```
[GroqMCP] Intent detected: create_task
[GroqMCP] MCP Tool: add_task -> Created task: buy groceries
```

### Check Database

Connect to your Neon database and verify tasks are being created:

```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

### Common Issues

#### Issue 1: "Groq API Error"

**Solution:**
- Check your `GROQ_API_KEY` in `.env`
- Verify you have Groq API credits
- Check internet connection

#### Issue 2: "Database Connection Error"

**Solution:**
- Verify `DATABASE_URL` in `.env`
- Check Neon database is running
- Run migrations: `alembic upgrade head`

#### Issue 3: "Intent Not Detected"

**Solution:**
- The fallback keyword matching should catch most intents
- Try more explicit commands: "Add a task to..." instead of just "Add..."
- Check backend logs for intent analysis results

#### Issue 4: "Task Not Found"

**Solution:**
- Verify task ID exists: "Show my tasks" first
- Use correct task ID in commands
- Check user authorization (tasks are user-specific)

## Performance Testing

### Test Response Times

```bash
# Test chat endpoint
curl -X POST http://localhost:7860/api/{user_id}/chat \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test performance"}'
```

Expected response time: 500-1000ms

### Load Testing

Use Apache Bench or similar:

```bash
ab -n 100 -c 10 -H "Authorization: Bearer {token}" \
  -p test_request.json \
  -T application/json \
  http://localhost:7860/api/{user_id}/chat
```

## Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads successfully
- [ ] User can sign up and sign in
- [ ] Chat interface displays correctly
- [ ] Add task command works
- [ ] List tasks command works
- [ ] Complete task command works
- [ ] Update task command works
- [ ] Delete task command works
- [ ] Tasks persist in database
- [ ] Conversation history is maintained
- [ ] Multiple users have isolated tasks
- [ ] Error handling works gracefully

## Success Criteria

Your Phase 3 implementation is successful if:

1. ✅ All 5 MCP tools execute correctly
2. ✅ Groq agent properly detects intents
3. ✅ Natural language responses are generated
4. ✅ Tasks are persisted in database
5. ✅ User authorization works correctly
6. ✅ Conversation history is maintained
7. ✅ Error handling is graceful
8. ✅ Response times are acceptable (<2s)

## Next Steps

After successful testing:

1. **Document your process** - Take screenshots of working chat
2. **Record a demo video** - Show all 5 MCP tools in action
3. **Prepare for submission** - Ensure all code is pushed to GitHub
4. **Write a summary** - Explain your architectural decisions

## Support

If you encounter issues:

1. Check backend logs: `tail -f backend.log`
2. Check frontend console: Browser DevTools (F12)
3. Verify environment variables: `cat .env`
4. Test database connection: `psql $DATABASE_URL`
5. Review this guide's troubleshooting section

## Conclusion

You now have a fully functional Phase 3 implementation with:
- ✅ Groq LLM integration
- ✅ MCP architecture with 5 tools
- ✅ Natural language interface
- ✅ Production-ready code

**Congratulations on completing Phase 3!** 🎉
