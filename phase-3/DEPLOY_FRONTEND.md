# Deploy Frontend to Vercel

## Quick Deploy

```bash
cd phase-3/frontend

# Install Vercel CLI (if not installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## During Deployment

When prompted:
- **Set up and deploy?** Yes
- **Which scope?** Your account
- **Link to existing project?** No
- **Project name?** speckit-hackathon-frontend (or your choice)
- **Directory?** ./
- **Override settings?** No

## Set Environment Variable

After deployment, set the environment variable:

```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://syeda-inshrah-speckit.hf.space
```

Then redeploy:
```bash
vercel --prod
```

## Your Deployed URLs

After deployment, you'll get:
- **Production URL:** https://speckit-hackathon-frontend.vercel.app (or similar)
- **Preview URL:** https://speckit-hackathon-frontend-xxx.vercel.app

## Test Your Deployment

1. Open your production URL
2. Sign up / Sign in
3. Go to Chat page
4. Test: "Add a task to buy groceries"
5. Verify it connects to your Hugging Face backend

## Troubleshooting

If the frontend can't connect to backend:
1. Check environment variable is set correctly
2. Verify Hugging Face backend is running
3. Check browser console for CORS errors
4. Ensure backend allows requests from your Vercel domain

## Update Backend CORS (if needed)

If you get CORS errors, update your backend to allow your Vercel domain:

```python
# In backend app.py or main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",  # Allow all Vercel preview URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
