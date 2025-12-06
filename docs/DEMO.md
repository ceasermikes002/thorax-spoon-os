# Thorax - Demo Guide

## 🎯 Quick Demo for Judges

This guide will help you quickly experience the key features of Thorax.

---

## 🚀 Starting the Application

### Backend
```bash
# From project root
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

---

## 📋 Demo Workflow

### 1. View the Dashboard
- Open http://localhost:3000
- Notice the **Health & Metrics** card showing:
  - SpoonOS availability ✓
  - Gemini configuration ✓
  - ElevenLabs configuration ✓
  - System metrics (events, breaches, API calls)

### 2. Register a Test Contract

**Example Neo Testnet Contract:**
- Contract Hash: `0x1234567890abcdef1234567890abcdef12345678`
- Network: `Testnet`
- Chain: `Neo`
- Owner Email: `your-email@example.com`

**Optional ABI for Enhanced Analysis:**
```json
{
  "methods": [
    {"name": "transfer", "parameters": [{"name": "to", "type": "Hash160"}, {"name": "amount", "type": "Integer"}]},
    {"name": "rescueFunds", "parameters": [{"name": "amount", "type": "Integer"}]},
    {"name": "emergencyWithdraw", "parameters": []}
  ]
}
```

Click **"Register Contract"** and observe:
- ✅ Form validation prevents empty submissions
- ✅ Real-time error feedback for invalid inputs
- ✅ AI analysis results showing:
  - Risk level (0-100%)
  - Identified breach vectors
  - Monitoring events
  - Legal compliance assessment

### 3. View AI Analysis
- Click **"View Analysis"** on the registered contract
- Review the detailed report:
  - Contract name/hash
  - Risk percentage
  - Breach vectors (e.g., "unauthorized_access", "fund_rescue")
  - Monitoring events (e.g., "Transfer", "EmergencyWithdraw")
  - Formatted AI-generated security report

### 4. Activate Monitoring
- Click **"Activate"** to enable real-time monitoring
- The system will:
  - Poll Neo blockchain for contract events
  - Analyze each event with SpoonOS AI agents
  - Detect potential security breaches
  - Send alerts for critical events

### 5. Monitor Events
- Click **"Monitor Once"** to trigger an immediate blockchain scan
- View events in the **Events** panel
- Filter by time range: 1 Week, 1 Month, 3 Months, All
- Each event shows:
  - Event name
  - Severity level
  - Breach detection status
  - Timestamp
  - AI-generated message
  - Recommended actions

### 6. Send Manual Alert
- Click **"Send Alert"** on any contract
- Enter a custom message
- Toggle voice synthesis option
- Click **"Send"** to email the contract owner

### 7. Real-Time Logs
- Scroll to the **Real-Time Logs** section
- Watch live monitoring events stream in
- See activation status, network info, block numbers, and breach detection

---

## 🎨 UI/UX Features to Notice

### Form Validation
- ✅ Required fields marked with asterisk (*)
- ✅ Real-time validation feedback
- ✅ Red borders and error messages for invalid inputs
- ✅ Email format validation
- ✅ JSON validation for ABI field
- ✅ Submit button disabled during processing

### Visual Design
- ✅ Modern dark theme with primary color accents
- ✅ Lucide icons throughout the interface
- ✅ Color-coded risk levels (green/yellow/red)
- ✅ Responsive grid layout
- ✅ Hover effects and transitions
- ✅ Status badges (Active/Inactive)
- ✅ Loading states for async operations

### Navigation
- ✅ Sticky header with shield logo
- ✅ Smooth transitions between pages
- ✅ Footer with hackathon information
- ✅ Help dialogs (?) for each section

---

## 📖 Documentation to Review

### How It Works Page
Visit http://localhost:3000/how-it-works to see:
- Comprehensive project overview
- Key features with icons and descriptions
- Technical architecture (4-step flow)
- SpoonOS integration details
- Neo blockchain integration
- Real-world use cases
- Technology stack
- Hackathon track alignment
- Future enhancements

---

## 🔍 Key Hackathon Features

### SpoonOS Integration ✓
- AI agents analyze contract ABIs autonomously
- Breach detection using SpoonOS reasoning
- Multi-agent orchestration for monitoring

### Neo Blockchain ✓
- Native Neo RPC integration
- Contract notification monitoring
- Testnet and mainnet support
- Multi-language contract compatibility

### AI Agent with Web3 ✓
- **Autonomy**: Agents monitor and analyze without human input
- **Security**: Risk scoring, severity classification, safeguards
- **Usefulness**: Solves real Web3 security challenges
- **On-Chain Interaction**: Monitors blockchain state and events

---

## 🎥 Demo Script for Presentation

1. **Introduction** (30 seconds)
   - "Thorax is an AI-powered security platform for Neo smart contracts"
   - "It combines SpoonOS agents with Neo blockchain for autonomous threat detection"

2. **Registration** (1 minute)
   - Show form validation by trying to submit empty form
   - Register a contract with sample data
   - Highlight AI analysis results

3. **Monitoring** (1 minute)
   - Activate the contract
   - Trigger "Monitor Once"
   - Show real-time logs streaming

4. **Documentation** (30 seconds)
   - Navigate to "How It Works"
   - Scroll through comprehensive documentation
   - Highlight SpoonOS and Neo integration sections

5. **Conclusion** (30 seconds)
   - Recap key features
   - Mention future enhancements
   - Thank judges

---

## 🐛 Troubleshooting

### Backend Issues
- Ensure PostgreSQL is running
- Check environment variables are set
- Run `prisma generate && prisma db push`

### Frontend Issues
- Ensure backend is running at http://localhost:8000
- Check `.env.local` has `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`
- Clear browser cache if needed

### No Events Showing
- This is expected if no real contracts are registered
- The demo focuses on the registration and analysis features
- Real monitoring requires actual Neo contracts with activity

---

## 📞 Support

For technical questions during judging, refer to:
- [README.md](./README.md) - Full setup instructions
- [HACKATHON.md](./HACKATHON.md) - Hackathon submission details
- Code comments in `app/main.py` and `frontend/app/page.tsx`

