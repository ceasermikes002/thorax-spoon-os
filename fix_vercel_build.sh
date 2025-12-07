#!/bin/bash

echo ""
echo "========================================"
echo "  Fixing Vercel Build Error"
echo "========================================"
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Remove frontend/lib from cache (if it was previously ignored)
echo "📦 Step 1: Removing frontend/lib from Git cache..."
git rm -r --cached frontend/lib/ 2>/dev/null || echo "   (frontend/lib not in cache, continuing...)"
echo ""

# Add updated .gitignore
echo "📝 Step 2: Adding updated .gitignore..."
git add .gitignore
echo "   ✅ .gitignore updated"
echo ""

# Force add frontend/lib files
echo "✅ Step 3: Force adding frontend/lib directory..."
git add -f frontend/lib/
git add -f frontend/lib/utils.ts
echo "   ✅ Added frontend/lib/"
echo ""

# Show what's staged
echo "📋 Step 4: Checking staged files..."
git status --short
echo ""

# Commit
echo "💾 Step 5: Committing changes..."
git commit -m "Fix: Allow frontend/lib directory in Git

- Updated .gitignore to not ignore frontend/lib/
- Added frontend/lib/utils.ts (required for build)
- Fixes Vercel build error: Module not found @/lib/utils"
echo ""

# Push
echo "🚀 Step 6: Pushing to GitHub..."
read -p "Push to which branch? (master/main) [master]: " branch
branch=${branch:-master}

git push origin $branch

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  SUCCESS!"
    echo "========================================"
    echo ""
    echo "frontend/lib is now in Git and Vercel should build successfully."
    echo ""
    echo "Next steps:"
    echo "1. Go to Vercel dashboard"
    echo "2. Trigger a new deployment"
    echo "3. Build should succeed now!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check the error message above."
    echo ""
fi

