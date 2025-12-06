# Email Setup Guide for Thorax

## 🚨 Issue: Emails Not Sending

If you're not receiving emails when sending alerts, it's because the SMTP configuration is missing.

---

## ✅ Solution: Configure Gmail SMTP

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google", enable **2-Step Verification**
4. Follow the prompts to set it up

### Step 2: Generate App Password

1. After enabling 2FA, go back to **Security**
2. Under "How you sign in to Google", click **App passwords**
3. Select **Mail** as the app
4. Select **Other (Custom name)** as the device
5. Enter "Thorax" as the name
6. Click **Generate**
7. **Copy the 16-character password** (you won't see it again!)

### Step 3: Create .env File

Create a `.env` file in the project root (same directory as `README.md`):

```bash
# Copy the example file
cp .env.example .env
```

### Step 4: Configure Email Settings

Edit the `.env` file and add your Gmail credentials:

```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=chimaemekamicheal@gmail.com
SMTP_PASSWORD=your-16-char-app-password-here
SMTP_FROM=chimaemekamicheal@gmail.com

# Also add your Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important:**
- Use the **App Password** (16 characters), NOT your regular Gmail password
- Don't include spaces in the app password
- Keep the `.env` file secret (it's already in `.gitignore`)

### Step 5: Restart the Backend

```bash
# Stop the backend (Ctrl+C)
# Then restart it
uvicorn app.main:app --reload
```

---

## 🧪 Testing Email Alerts

### Method 1: Via Frontend

1. Register a contract with your email: `chimaemekamicheal@gmail.com`
2. Click "Send Alert" on the contract
3. Enter a test message
4. Click "Send Alert"
5. Check your Gmail inbox (and spam folder)

### Method 2: Via API

```bash
# First, get a contract ID
curl http://localhost:8000/contracts

# Then send an alert
curl -X POST http://localhost:8000/notify \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "your-contract-id-here",
    "message": "Test alert from Thorax",
    "voice": false
  }'
```

---

## 🔍 Troubleshooting

### Issue: "SMTP not configured" error

**Solution:** Make sure all SMTP environment variables are set in `.env`:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM`

### Issue: "Authentication failed" error

**Solutions:**
1. Make sure you're using the **App Password**, not your regular password
2. Verify 2-Factor Authentication is enabled on your Google account
3. Try generating a new App Password
4. Check for typos in the `.env` file

### Issue: Email sent but not received

**Solutions:**
1. Check your **Spam/Junk** folder
2. Check Gmail's **All Mail** folder
3. Verify the email address in the contract is correct
4. Check backend logs for errors:
   ```bash
   # Look for email-related errors in the terminal
   ```

### Issue: "Connection refused" error

**Solutions:**
1. Check your internet connection
2. Verify `SMTP_HOST=smtp.gmail.com` and `SMTP_PORT=587`
3. Make sure your firewall isn't blocking port 587
4. Try using port 465 with SSL (less common)

---

## 📧 Alternative Email Providers

### Using Outlook/Hotmail

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_FROM=your-email@outlook.com
```

### Using SendGrid

```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM=your-verified-sender@example.com
```

### Using Mailgun

```env
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-smtp-password
SMTP_FROM=noreply@your-domain.com
```

---

## ✅ Verification

Once configured correctly, you should see:

1. **In the alert dialog:** Your email address displayed prominently
2. **In backend logs:** "Email sent successfully" messages
3. **In your inbox:** Alert emails with subject "Thorax Manual Alert: [Contract Name]"

---

## 🔒 Security Notes

- Never commit your `.env` file to Git
- Use App Passwords instead of your main password
- Rotate your App Password periodically
- Consider using a dedicated email account for the application

---

## 📝 Email Template

Emails sent by Thorax include:

**Subject:** `Thorax Manual Alert: [Contract Name]`

**Body:**
```
[Your custom message]

Contract: [Contract Hash]
Sent from Thorax Security Platform
```

For breach alerts:
```
Breach detected on contract [hash]
Event: [Event Name]
Severity: [critical/high/medium/low]
Reason: [AI analysis]
Recommended Action: [AI recommendation]
```

---

Need help? Check the backend logs for detailed error messages!

