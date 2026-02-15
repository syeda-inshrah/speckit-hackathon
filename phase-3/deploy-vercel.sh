#!/bin/bash
# Quick Vercel Deployment Script for Phase 3 Frontend

echo "🚀 Deploying Phase 3 Frontend to Vercel..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Logging in to Vercel..."
vercel login

# Deploy to production
echo "🌐 Deploying to production..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Don't forget to set environment variable:"
echo "   vercel env add NEXT_PUBLIC_API_URL production"
echo "   Value: https://syeda-inshrah-speckit.hf.space"
echo ""
echo "Then redeploy:"
echo "   vercel --prod"
