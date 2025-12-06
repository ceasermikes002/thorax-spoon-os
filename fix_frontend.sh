#!/bin/bash

echo "🔧 Fixing frontend visibility on GitHub..."
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Remove frontend from cache (if it was previously ignored)
echo "📦 Step 1: Removing frontend from Git cache..."
git rm -r --cached frontend/ 2>/dev/null || echo "   (frontend not in cache, continuing...)"
echo ""

# Add updated .gitignore
echo "📝 Step 2: Adding updated .gitignore..."
git add .gitignore
echo "   ✅ .gitignore updated"
echo ""

# Force add frontend files
echo "✅ Step 3: Adding frontend files..."
git add -f frontend/app/ 2>/dev/null && echo "   ✅ Added frontend/app/"
git add -f frontend/components/ 2>/dev/null && echo "   ✅ Added frontend/components/"
git add -f frontend/lib/ 2>/dev/null && echo "   ✅ Added frontend/lib/"
git add -f frontend/public/ 2>/dev/null && echo "   ✅ Added frontend/public/"
git add -f frontend/*.json 2>/dev/null && echo "   ✅ Added frontend/*.json"
git add -f frontend/*.ts 2>/dev/null && echo "   ✅ Added frontend/*.ts"
git add -f frontend/*.mjs 2>/dev/null && echo "   ✅ Added frontend/*.mjs"
git add -f frontend/*.js 2>/dev/null && echo "   ✅ Added frontend/*.js"
echo ""

# Show what's staged
echo "📋 Step 4: Checking staged files..."
git status --short
echo ""

# Commit
echo "💾 Step 5: Committing changes..."
git commit -m "Fix: Add frontend directory and update .gitignore

- Updated .gitignore to only ignore specific frontend files (.next/, out/, .env)
- Added frontend source code to repository
- Frontend is now properly tracked and visible on GitHub"
echo ""

# Push
echo "🚀 Step 6: Pushing to GitHub..."
read -p "Push to which branch? (master/main) [master]: " branch
branch=${branch:-master}

git push origin $branch

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Frontend should now be visible on GitHub."
    echo ""
    echo "🔗 Check here:"
    echo "   https://github.com/ceasermikes002/thorax-spoon-os/tree/$branch/frontend"
    echo ""
    echo "⏳ Note: It may take a few seconds for GitHub to update."
else
    echo ""
    echo "❌ Push failed. Please check the error message above."
    echo ""
    echo "Common issues:"
    echo "  - Wrong branch name (try 'main' instead of 'master')"
    echo "  - Authentication required (check your GitHub credentials)"
    echo "  - Network issues (check your internet connection)"
fi

