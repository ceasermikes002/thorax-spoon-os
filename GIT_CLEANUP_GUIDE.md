# Git Cleanup Guide - Remove Sensitive Files

## 🚨 IMPORTANT: You mentioned you committed without .gitignore!

If you've committed sensitive files (like `.env` with API keys), follow this guide to clean up your Git history.

---

## ⚠️ Files That Should NEVER Be Committed

- `.env` - Contains API keys, passwords, database credentials
- `venv/` - Python virtual environment (large, unnecessary)
- `node_modules/` - Node.js dependencies (huge, unnecessary)
- `__pycache__/` - Python cache files
- `.pytest_cache/` - Test cache
- `*.log` - Log files
- Database files (`.db`, `.sqlite`)

---

## 🔍 Step 1: Check What You've Committed

```bash
# See all files in your repository
git ls-files

# Check if .env is committed (DANGEROUS!)
git ls-files | grep .env

# Check if venv is committed (LARGE!)
git ls-files | grep venv

# Check if node_modules is committed (HUGE!)
git ls-files | grep node_modules
```

---

## 🧹 Step 2: Remove Sensitive Files from Git History

### Option A: If You Haven't Pushed Yet (EASY)

```bash
# Remove .env from staging
git rm --cached .env

# Remove venv from staging
git rm --cached -r venv/

# Remove node_modules from staging
git rm --cached -r frontend/node_modules/

# Remove __pycache__
git rm --cached -r __pycache__/

# Commit the removal
git commit -m "Remove sensitive and unnecessary files"
```

### Option B: If You've Already Pushed (HARDER)

**WARNING:** This rewrites Git history. Only do this if you're the only contributor!

```bash
# Remove .env from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Remove venv from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch -r venv/" \
  --prune-empty --tag-name-filter cat -- --all

# Remove node_modules from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch -r frontend/node_modules/" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGEROUS - only if you're alone!)
git push origin --force --all
```

### Option C: Use BFG Repo-Cleaner (RECOMMENDED for large files)

```bash
# Install BFG
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove .env
java -jar bfg.jar --delete-files .env

# Remove folders
java -jar bfg.jar --delete-folders venv
java -jar bfg.jar --delete-folders node_modules
java -jar bfg.jar --delete-folders __pycache__

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
```

---

## 🔒 Step 3: Rotate Your API Keys (CRITICAL!)

If you committed `.env` with API keys, **you must rotate them immediately**:

### Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Delete the old key
3. Create a new key
4. Update your local `.env` file

### ElevenLabs API Key
1. Go to https://elevenlabs.io/app/settings/api-keys
2. Revoke the old key
3. Generate a new key
4. Update your local `.env` file

### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Revoke the old password
3. Generate a new one
4. Update your local `.env` file

---

## ✅ Step 4: Verify Cleanup

```bash
# Check that sensitive files are gone
git ls-files | grep .env
# Should return nothing

git ls-files | grep venv
# Should return nothing

git ls-files | grep node_modules
# Should return nothing

# Check repository size
du -sh .git
# Should be much smaller now
```

---

## 📝 Step 5: Add .gitignore and Commit

```bash
# .gitignore is already created in the root directory

# Add it to Git
git add .gitignore

# Commit
git commit -m "Add .gitignore to prevent committing sensitive files"

# Push
git push origin main
```

---

## 🔄 Step 6: Create .env from .env.example

```bash
# Copy the example
cp .env.example .env

# Edit with your NEW API keys (after rotation)
nano .env
# or
code .env

# Verify .env is NOT tracked
git status
# Should NOT show .env
```

---

## 🎯 Quick Cleanup Script

Save this as `cleanup.sh` and run it:

```bash
#!/bin/bash

echo "🧹 Cleaning up Git repository..."

# Remove sensitive files
git rm --cached .env 2>/dev/null
git rm --cached -r venv/ 2>/dev/null
git rm --cached -r frontend/node_modules/ 2>/dev/null
git rm --cached -r __pycache__/ 2>/dev/null
git rm --cached -r .pytest_cache/ 2>/dev/null
git rm --cached -r frontend/.next/ 2>/dev/null

# Add .gitignore
git add .gitignore

# Commit
git commit -m "Remove sensitive files and add .gitignore"

echo "✅ Cleanup complete!"
echo "⚠️  Remember to rotate your API keys if .env was committed!"
```

Run it:
```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## 🚨 Emergency: If API Keys Were Exposed

### Immediate Actions:

1. **Rotate ALL API keys** (see Step 3)
2. **Check for unauthorized usage:**
   - Google Cloud Console: Check API usage
   - ElevenLabs: Check usage dashboard
   - Gmail: Check sent emails

3. **Monitor for abuse:**
   - Set up billing alerts
   - Check for unusual activity
   - Review access logs

4. **Consider:**
   - Enabling 2FA on all accounts
   - Using environment variable management tools (e.g., Doppler, Vault)
   - Setting up API key restrictions (IP whitelist, usage limits)

---

## ✅ Prevention Checklist

- [x] `.gitignore` file created
- [ ] `.env` removed from Git
- [ ] `venv/` removed from Git
- [ ] `node_modules/` removed from Git
- [ ] `__pycache__/` removed from Git
- [ ] API keys rotated (if exposed)
- [ ] `.env.example` committed (safe template)
- [ ] Repository size reduced
- [ ] Git history cleaned

---

## 📚 Best Practices Going Forward

1. **Always create `.gitignore` FIRST** before any commits
2. **Never commit `.env` files** - use `.env.example` instead
3. **Use environment variable managers** for production
4. **Review `git status`** before every commit
5. **Use `git add -p`** to review changes interactively
6. **Set up pre-commit hooks** to prevent sensitive file commits

---

## 🆘 Need Help?

If you're stuck, check:
- Git status: `git status`
- Git log: `git log --oneline`
- Files tracked: `git ls-files`

**Still stuck?** The `.gitignore` is now in place. Just make sure to:
1. Remove any committed sensitive files
2. Rotate exposed API keys
3. Continue development safely

---

Good luck! 🚀

