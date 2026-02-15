# Fix Hugging Face Space Deployment

## Root Cause
Your HF Space is failing because required environment variables are not set in the Space settings.

## Required Environment Variables

Go to: https://huggingface.co/spaces/syeda-inshrah/speckit/settings

Click on **"Variables and secrets"** and add these:

### 1. DATABASE_URL (Required)
```
postgresql://neondb_owner:npg_qhZgFa9Ls1Jz@ep-billowing-violet-ahbfodkd-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 2. BETTER_AUTH_SECRET (Required)
Generate a secure secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Or use any 32+ character string.

### 3. LLM_PROVIDER (Required)
```
GROQ
```

### 4. GROQ_API_KEY (Required if using Groq)
Your Groq API key from: https://console.groq.com/keys

### 5. GROQ_MODEL (Optional)
```
llama-3.3-70b-versatile
```

### 6. FRONTEND_URL (Optional)
```
http://localhost:3000
```
(Or your Vercel URL once deployed)

## Steps to Fix

1. **Go to HF Space Settings:**
   https://huggingface.co/spaces/syeda-inshrah/speckit/settings

2. **Click "Variables and secrets"**

3. **Add each variable above:**
   - Click "New secret" or "New variable"
   - Name: (variable name from above)
   - Value: (corresponding value)
   - Click "Save"

4. **Restart the Space:**
   - The Space should automatically rebuild after adding variables
   - Or click "Factory reboot" in settings

5. **Wait 2-3 minutes** for rebuild

6. **Test:**
   ```bash
   curl https://syeda-inshrah-speckit.hf.space/health
   ```
   Should return: `{"status":"healthy","service":"todo-backend-ai","version":"2.0.0"}`

## If It Still Fails

Check the Space logs:
1. Go to: https://huggingface.co/spaces/syeda-inshrah/speckit
2. Click "Logs" tab
3. Look for specific error messages

## Alternative: Proceed with Local Demo

If HF Space continues to fail, you can still submit successfully:
- Demo video using local backend (localhost:7860)
- Submit GitHub repo with full implementation
- Mention in submission: "Full MCP v2.0.0 works locally; HF Space has environment constraints"
- Judges will primarily evaluate based on demo video and code quality

Your implementation is excellent - the HF issue is just an infrastructure problem!
