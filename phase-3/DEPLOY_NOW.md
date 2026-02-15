# Deploy Frontend to Vercel - Final Steps

## ✅ Prerequisites Complete
- [x] Vercel CLI installed
- [x] Frontend code ready
- [x] Backend deployed on Hugging Face: https://syeda-inshrah-speckit.hf.space
- [x] Environment variable configured in .env.local

## 🚀 Deploy Now (3 Steps)

### Step 1: Login to Vercel
```bash
cd phase-3/frontend
vercel login
```
This will open your browser. Click "Continue with GitHub" or your preferred method.

### Step 2: Deploy to Production
```bash
vercel --prod
```

When prompted:
- **Set up and deploy?** → Yes
- **Which scope?** → Select your account
- **Link to existing project?** → No
- **Project name?** → `speckit-hackathon-frontend` (or your choice)
- **Directory?** → `./` (press Enter)
- **Override settings?** → No (press Enter)

### Step 3: Set Environment Variable
```bash
vercel env add NEXT_PUBLIC_API_URL production
```
When prompted, enter: `https://syeda-inshrah-speckit.hf.space`

Then redeploy to apply the environment variable:
```bash
vercel --prod
```

## 📝 Your Deployment URL
After deployment, you'll get a URL like:
```
https://speckit-hackathon-frontend.vercel.app
```

Copy this URL - you'll need it for the hackathon submission form!

## ✅ Test Your Deployment
1. Open your Vercel URL
2. Sign up / Sign in
3. Go to Chat page
4. Test: "Add a task to buy groceries"
5. Verify it works with your Hugging Face backend

## 📤 Next Steps After Deployment
1. ✅ Deploy frontend to Vercel (you're doing this now!)
2. ⏭️ Create demo video (max 90 seconds)
3. ⏭️ Submit form: https://forms.gle/KMKEKaFUD6ZX4UtY8

---

## 🎥 Demo Video Outline (90 seconds)

**0-15s:** Introduction
- "Phase 3: AI-Powered Todo Chatbot"
- "Using Groq + MCP Architecture"

**15-30s:** Add Tasks
- Type: "Add a task to buy groceries"
- Show: ✓ Created task confirmation

**30-45s:** List Tasks
- Type: "Show me all my tasks"
- Show: Task list displayed

**45-60s:** Complete & Update
- Type: "Mark task 1 as complete"
- Type: "Update task 2 title to 'Finish report'"

**60-75s:** Delete Task
- Type: "Delete task 3"
- Show: Deletion confirmation

**75-90s:** Architecture Highlight
- Show: "Groq LLM → MCP Tools → Database"
- Mention: "5 MCP tools, stateless architecture"

---

## 📋 Submission Form Information

**Form URL:** https://forms.gle/KMKEKaFUD6ZX4UtY8

**What to Submit:**
1. GitHub Repository: `https://github.com/syeda-inshrah/speckit-hackathon`
2. Backend URL: `https://syeda-inshrah-speckit.hf.space`
3. Frontend URL: `https://your-app.vercel.app` (get this after deployment)
4. Demo Video: Upload to YouTube (unlisted) and paste link
5. WhatsApp Number: For presentation invitation

---

## 🎯 You're Almost Done!

Your Phase 3 is **95% complete**. Just:
1. Run the 3 deployment commands above
2. Create the 90-second demo video
3. Submit the form

**Good luck with your submission!** 🚀
