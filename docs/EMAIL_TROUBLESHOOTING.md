# Email Troubleshooting Guide

## 🚨 Problem: Emails Not Sending

If you're not receiving email alerts, follow this step-by-step troubleshooting guide.

---

## ✅ Step 1: Verify .env File Exists

```bash
# Check if .env file exists in project root
ls -la .env

# If not found, create it
cp .env.example .env
```

**Expected output:**
```
-rw-r--r-- 1 user user 256 Dec 7 .env
```

---

## ✅ Step 2: Check .env Configuration

```bash
# View your SMTP settings (without showing password)
cat .env | grep SMTP
```

**Should show:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM=your-email@gmail.com
```

**Common Issues:**
- ❌ Missing SMTP variables → Add them to .env
- ❌ Wrong email format → Use full Gmail address
- ❌ Regular password instead of App Password → Generate App Password
- ❌ Spaces in App Password → Remove all spaces (should be 16 characters)

---

## ✅ Step 3: Generate Gmail App Password

**You MUST use an App Password, not your regular Gmail password!**

1. **Enable 2FA first:**
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Thorax" as the name
   - Click "Generate"
   - **Copy the 16-character password** (no spaces!)

3. **Add to .env:**
   ```env
   SMTP_PASSWORD=abcdefghijklmnop  # 16 characters, no spaces
   ```

---

## ✅ Step 4: Test SMTP Connection

Create a test file `test_email.py`:

```python
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing SMTP connection...")
print(f"SMTP_HOST: {os.getenv('SMTP_HOST')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
print(f"SMTP_USER: {os.getenv('SMTP_USER')}")
print(f"SMTP_PASSWORD: {'*' * len(os.getenv('SMTP_PASSWORD', ''))}")

try:
    # Connect to SMTP server
    server = smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT')))
    server.starttls()
    
    # Login
    server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
    print("✅ SMTP login successful!")
    
    # Send test email
    msg = MIMEText("This is a test email from Thorax")
    msg['Subject'] = "Thorax Test Email"
    msg['From'] = os.getenv('SMTP_FROM')
    msg['To'] = os.getenv('SMTP_USER')
    
    server.send_message(msg)
    print("✅ Test email sent successfully!")
    
    server.quit()
    print("\n✅ All tests passed! Email is configured correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nCommon fixes:")
    print("1. Make sure 2FA is enabled on your Gmail account")
    print("2. Generate an App Password (not your regular password)")
    print("3. Check for typos in .env file")
    print("4. Make sure .env is in the project root directory")
```

Run it:
```bash
python test_email.py
```

**Expected output:**
```
Testing SMTP connection...
SMTP_HOST: smtp.gmail.com
SMTP_PORT: 587
SMTP_USER: your-email@gmail.com
SMTP_PASSWORD: ****************
✅ SMTP login successful!
✅ Test email sent successfully!
✅ All tests passed! Email is configured correctly.
```

---

## ✅ Step 5: Restart Backend

After updating .env, restart the backend:

```bash
# Stop the backend (Ctrl+C)
# Then restart
uvicorn app.main:app --reload
```

**Why?** The backend loads .env on startup. Changes won't take effect until restart.

---

## ✅ Step 6: Test from Thorax UI

1. Open http://localhost:3000
2. Register a contract with your email
3. Click "Send Alert" button
4. Check your email inbox (and spam folder!)

---

## 🔍 Common Error Messages

### Error: "Authentication failed"
**Cause:** Wrong password or not using App Password
**Fix:** Generate App Password at https://myaccount.google.com/apppasswords

### Error: "Username and Password not accepted"
**Cause:** 2FA not enabled or wrong credentials
**Fix:** 
1. Enable 2FA on Gmail
2. Generate new App Password
3. Update .env with new password
4. Restart backend

### Error: "Connection refused"
**Cause:** Wrong SMTP host or port
**Fix:** Use `smtp.gmail.com` and port `587`

### Error: "No module named 'dotenv'"
**Cause:** Missing python-dotenv package
**Fix:** `pip install python-dotenv`

### Error: ".env file not found"
**Cause:** .env file not in project root
**Fix:** Create .env in same directory as README.md

---

## 📋 Complete .env Template

```env
# Email Configuration (Required for alerts)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM=your-email@gmail.com

# AI Configuration (Required for analysis)
GEMINI_API_KEY=your_gemini_api_key_here

# Voice Synthesis (Optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Database (Optional - uses SQLite by default)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/thorax
```

---

## ✅ Verification Checklist

- [ ] 2FA enabled on Gmail account
- [ ] App Password generated (16 characters)
- [ ] .env file exists in project root
- [ ] SMTP_USER is your full Gmail address
- [ ] SMTP_PASSWORD is App Password (not regular password)
- [ ] No spaces in App Password
- [ ] Backend restarted after .env changes
- [ ] Test script runs successfully
- [ ] Email received in inbox

---

## 🆘 Still Not Working?

### Check Gmail Security Settings

1. Go to https://myaccount.google.com/security
2. Check "Recent security activity"
3. Look for blocked sign-in attempts
4. If blocked, click "Yes, it was me"

### Check Spam Folder

Thorax emails might be in spam initially. Mark as "Not Spam" to fix.

### Try Different Email

If your Gmail has strict security, try:
1. Creating a new Gmail account
2. Enable 2FA
3. Generate App Password
4. Use that account in .env

### Check Backend Logs

```bash
# Run backend with verbose logging
uvicorn app.main:app --reload --log-level debug
```

Look for SMTP errors in the output.

---

## ✅ Success!

Once emails are working, you should see:
- ✅ Test email received
- ✅ Alert emails from Thorax
- ✅ No errors in backend logs

**Now you can use the voice alert feature in the webapp!** 🎉

