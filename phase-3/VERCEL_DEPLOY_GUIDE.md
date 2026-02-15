# Deploy Frontend to Vercel - Step by Step

## Prerequisites ✅
- Vercel CLI installed (v50.17.1)
- Frontend code ready
- Backend running (local or HF Space)

## Deployment Steps

### Step 1: Open Terminal in Frontend Directory
```bash
cd D:\hackathon-02\phase-3\frontend
```

### Step 2: Login to Vercel
```bash
vercel login
```
This will open your browser. Choose your authentication method (GitHub recommended).

### Step 3: Deploy to Production
```bash
vercel --prod
```

**When prompted, answer:**
- **Set up and deploy?** → Yes (press Enter)
- **Which scope?** → Select your account (press Enter)
- **Link to existing project?** → No (press N)
- **Project name?** → `speckit-hackathon-frontend` (or your choice)
- **In which directory is your code located?** → `./` (press Enter)
- **Want to override settings?** → No (press N)

### Step 4: Wait for Deployment
Vercel will:
1. Build your Next.js app
2. Deploy to production
3. Give you a URL like: `https://speckit-hackathon-frontend.vercel.app`

### Step 5: Set Environment Variable
```bash
vercel env add NEXT_PUBLIC_API_URL production
```
**When prompted, enter:**
```
https://syeda-inshrah-speckit.hf.space
```
(Or `http://localhost:7860` if HF Space isn't working)

### Step 6: Redeploy with Environment Variable
```bash
vercel --prod
```

## Your Deployment URL
After deployment, you'll get a URL like:
```
https://speckit-hackathon-frontend-xxx.vercel.app
```

**Copy this URL** - you'll need it for the hackathon submission!

## Test Your Deployment
1. Open your Vercel URL in browser
2. Sign up / Sign in
3. Go to Chat page
4. Test: "Add a task to buy groceries"
5. Verify it connects to your backend

## Troubleshooting

### If frontend can't connect to backend:
1. Check environment variable is set correctly
2. Verify backend is running (HF Space or local)
3. Check browser console for CORS errors

### If you get CORS errors:
Your backend needs to allow your Vercel domain. This is already configured if you set `FRONTEND_URL` in HF Space settings.

## Next Steps After Deployment
1. ✅ Frontend deployed to Vercel
2. ⏭️ Record demo video (90 seconds)
3. ⏭️ Submit to hackathon form

---

## Ready to Deploy?

Open a new terminal window and run:
```bash
cd D:\hackathon-02\phase-3\frontend
vercel login
vercel --prod
```

Let me know when you've completed the deployment and I'll help with the next steps!
