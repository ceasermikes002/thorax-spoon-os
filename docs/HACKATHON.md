# Thorax - Hackathon Submission

## 🏆 SpoonOS & Neo Hackathon - AI Agent with Web3 Track

**Thorax** is an AI-powered smart contract security platform that provides real-time monitoring, risk analysis, and automated threat detection for Neo blockchain contracts.

---

## 🎯 Project Overview

Thorax combines **SpoonOS AI agents** with **Neo blockchain infrastructure** to create an autonomous security monitoring system. The platform analyzes smart contracts for vulnerabilities, monitors blockchain events in real-time, and sends intelligent alerts when suspicious activities are detected.

### Key Innovation
- **Autonomous AI Agents**: SpoonOS-powered agents that independently analyze contract code, monitor blockchain state, and make security decisions
- **Real-Time Threat Detection**: Continuous monitoring of Neo blockchain with AI-driven breach analysis
- **Multi-Modal Alerts**: Email notifications with optional AI-generated voice synthesis for critical events
- **Legal Compliance Analysis**: Automated evaluation of contract fairness and regulatory compliance

---

## ✅ Hackathon Requirements Met

### Main Track: SpoonOS Components ✓
- ✅ **SpoonOS AI Agent Framework**: Autonomous agents for contract analysis and threat detection
- ✅ **LLM Integration**: Combined SpoonOS with Google Gemini for advanced reasoning
- ✅ **Agent Orchestration**: Multi-agent system for monitoring, analysis, and alerting

### Track: AI Agent with Web3 ✓
- ✅ **Autonomy**: AI agents independently monitor blockchain and trigger alerts without manual input
- ✅ **Security**: Risk scoring, severity classification, and safeguards against false positives
- ✅ **Usefulness**: Solves real Web3 security challenges with automated contract monitoring
- ✅ **Neo Integration**: Native Neo RPC integration, contract notification monitoring, testnet/mainnet support

### Neo Blockchain Integration ✓
- ✅ **Neo RPC**: Direct integration with Neo nodes for real-time data
- ✅ **Contract Notifications**: Monitors Neo's native notification system
- ✅ **Multi-Network**: Supports both testnet and mainnet deployments
- ✅ **Multi-Language**: Compatible with C#, Python, and other Neo-supported languages via ABI

---

## 🚀 Features

### 1. AI-Powered Contract Analysis
- **Risk Scoring**: 0-10 scale risk assessment using SpoonOS + Gemini
- **Breach Vector Detection**: Identifies potential attack surfaces (reentrancy, overflow, unauthorized access)
- **Method Analysis**: Flags dangerous functions (rescueFunds, emergencyWithdraw, selfDestruct)
- **Legal Compliance**: Evaluates contract fairness and user protection

### 2. Real-Time Monitoring
- **Blockchain Polling**: Scans recent blocks for contract events
- **Event Filtering**: Matches notifications against registered contracts
- **AI Breach Detection**: Each event analyzed for security threats
- **Severity Classification**: Events categorized as low/medium/high/critical

### 3. Automated Alerts
- **Email Notifications**: Sent to contract owners with event details
- **Voice Synthesis**: Optional audio alerts via ElevenLabs for critical events
- **Recommended Actions**: AI provides specific mitigation steps
- **Real-Time Dashboard**: Live logs and event history

### 4. User-Friendly Interface
- **Next.js Frontend**: Modern, responsive UI with shadcn/ui components
- **Form Validation**: Prevents empty submissions with real-time error feedback
- **Visual Indicators**: Icons, color-coded risk levels, and status badges
- **Comprehensive Documentation**: Detailed "How It Works" page

---

## 🛠️ Technology Stack

### Frontend
- **Next.js 16** (React 19)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Lucide Icons**

### Backend
- **FastAPI** (Python)
- **Prisma ORM**
- **PostgreSQL**
- **Neo3-Python SDK**
- **Web3.py** (EVM support)

### AI & Services
- **SpoonOS** AI Agent Framework
- **Google Gemini** LLM
- **ElevenLabs** Voice AI
- **SMTP** Email Service

---

## 📊 Judging Criteria Alignment

### Idea (5/5)
- ✅ Addresses real Web3 security challenges
- ✅ Novel combination of AI agents + blockchain monitoring
- ✅ Feasible and sustainable with clear use cases (DeFi, NFT, DAO security)

### Technical Execution (5/5)
- ✅ Working demo with full functionality
- ✅ Implements SpoonOS AI agents as required
- ✅ Elegant solution using autonomous agents for complex security analysis
- ✅ Native Neo blockchain integration

### Presentation and Documentation (5/5)
- ✅ Polished UI/UX with modern design
- ✅ Comprehensive documentation covering purpose, architecture, and use cases
- ✅ Clear explanation of limitations and future enhancements
- ✅ Detailed "How It Works" page for judges and users

### Wow Factor (5/5)
- ✅ Multi-modal alerts (email + AI voice synthesis)
- ✅ Real-time AI-driven threat detection
- ✅ Autonomous agent decision-making
- ✅ Legal compliance analysis feature

---

## 🎥 Demo Workflow

1. **Register Contract**: Enter contract hash, network, and email
2. **AI Analysis**: View risk score, breach vectors, and legal assessment
3. **Activate Monitoring**: Enable real-time blockchain scanning
4. **Receive Alerts**: Get notified of suspicious events with AI recommendations
5. **Review Events**: Analyze historical events with time-range filtering

---

## 🔮 Future Enhancements

- **Automated Response Actions**: AI agents execute on-chain transactions to pause contracts
- **Multi-Chain Expansion**: Extend to Ethereum, Polygon, and other EVM chains
- **Predictive Analytics**: ML models to predict vulnerabilities before exploitation
- **Community Threat Intelligence**: Shared database of attack patterns
- **Neo Oracle Integration**: Leverage native oracles for enhanced threat assessment
- **Mobile App**: iOS/Android for on-the-go monitoring

---

## 🏗️ Setup & Installation

See [README.md](./README.md) for detailed setup instructions.

---

## 👥 Team

Built for the SpoonOS & Neo Hackathon at Encode Hub

---

## 📄 License

MIT License - Built for educational and hackathon purposes

