"use client";
import { Shield, Brain, Bell, Activity, FileText, Zap, Lock, Globe, Code, CheckCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function HowItWorks() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="relative">
            <div className="absolute inset-0 bg-primary/10 blur-lg rounded-full"></div>
            <Shield className="h-12 w-12 text-primary relative" />
          </div>
          <h1 className="text-5xl font-bold tracking-tight">
            How Thorax Works
          </h1>
        </div>
        <p className="text-muted-foreground">
          AI-Powered Smart Contract Monitoring and Security Analysis for Neo Blockchain
        </p>
      </div>

      {/* Overview Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <Activity className="h-6 w-6 text-primary" />
          Overview
        </h2>
        <div className="prose prose-invert max-w-none">
          <p className="text-muted-foreground leading-relaxed">
            <strong className="text-primary">Thorax</strong> is an intelligent blockchain security platform that combines <strong>AI agents</strong> with <strong>Web3 infrastructure</strong> to provide real-time monitoring,
            risk analysis, and automated alerts for smart contracts deployed on the Neo blockchain. Built for the SpoonOS and Neo Hackathon,
            this application demonstrates the power of AI-driven contract analysis and autonomous monitoring systems.
          </p>
        </div>
      </section>

      {/* Key Features */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
          <Zap className="h-6 w-6 text-primary" />
          Key Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Brain className="h-5 w-5 text-primary" />
                AI-Powered Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Leverages SpoonOS AI agents and Google Gemini to analyze smart contract ABIs, identify potential security risks,
              detect breach vectors, and provide intelligent recommendations for contract safety.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Activity className="h-5 w-5 text-primary" />
                Real-Time Monitoring
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Continuously monitors Neo blockchain for contract events, automatically detecting suspicious activities,
              analyzing transaction patterns, and triggering alerts when potential security breaches are identified.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Bell className="h-5 w-5 text-primary" />
                Automated Alerts
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Sends email notifications with optional AI-generated voice synthesis (via ElevenLabs) to contract owners
              when security events are detected, ensuring immediate awareness of critical issues.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <FileText className="h-5 w-5 text-primary" />
                Legal Compliance Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Analyzes smart contracts for legal fairness, regulatory compliance, and potential user protection issues,
              providing detailed reports on contract terms and recommended improvements.
            </CardContent>
          </Card>
        </div>
      </section>

      {/* How It Works - Technical Flow */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
          <Code className="h-6 w-6 text-primary" />
          Technical Architecture
        </h2>
        <div className="space-y-6">
          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">1. Contract Registration</h3>
            <p className="text-muted-foreground">
              Users register smart contracts by providing the contract hash and network (testnet/mainnet).
              The system supports both Neo and EVM chains. Upon registration, the contract ABI is analyzed using:
            </p>
            <ul className="list-disc list-inside mt-2 text-muted-foreground space-y-1">
              <li><strong>SpoonOS AI Agents:</strong> Autonomous agents analyze contract methods, parameters, and potential vulnerabilities</li>
              <li><strong>Google Gemini:</strong> Advanced LLM provides risk scoring (0-10 scale) and identifies breach vectors</li>
              <li><strong>Legal Analysis:</strong> Evaluates contract fairness, user protection, and regulatory compliance</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">2. Risk Assessment</h3>
            <p className="text-muted-foreground">
              The AI analysis engine evaluates multiple risk factors:
            </p>
            <ul className="list-disc list-inside mt-2 text-muted-foreground space-y-1">
              <li><strong>Method Analysis:</strong> Identifies dangerous functions (e.g., rescueFunds, emergencyWithdraw, selfDestruct)</li>
              <li><strong>Access Control:</strong> Checks for proper authorization and ownership mechanisms</li>
              <li><strong>Breach Vectors:</strong> Detects potential attack surfaces (reentrancy, overflow, unauthorized access)</li>
              <li><strong>Monitoring Events:</strong> Determines which contract events should trigger alerts</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">3. Continuous Monitoring</h3>
            <p className="text-muted-foreground">
              Once activated, contracts are monitored in real-time:
            </p>
            <ul className="list-disc list-inside mt-2 text-muted-foreground space-y-1">
              <li><strong>Neo RPC Polling:</strong> Scans recent blocks for contract notifications and events</li>
              <li><strong>Event Filtering:</strong> Matches blockchain events against registered contract addresses</li>
              <li><strong>AI Breach Detection:</strong> Each event is analyzed by SpoonOS agents to determine if it represents a security threat</li>
              <li><strong>Severity Classification:</strong> Events are categorized (low, medium, high, critical) based on risk level</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">4. Alert & Response</h3>
            <p className="text-muted-foreground">
              When suspicious activity is detected:
            </p>
            <ul className="list-disc list-inside mt-2 text-muted-foreground space-y-1">
              <li><strong>Email Notifications:</strong> Sent to contract owner with event details and AI analysis</li>
              <li><strong>Voice Synthesis:</strong> Optional audio alerts generated via ElevenLabs for critical events</li>
              <li><strong>Recommended Actions:</strong> AI provides specific steps to mitigate detected threats</li>
              <li><strong>Dashboard Updates:</strong> Real-time logs and event history displayed in the UI</li>
            </ul>
          </div>
        </div>
      </section>

      {/* SpoonOS Integration */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
          <Brain className="h-6 w-6 text-primary" />
          SpoonOS Integration (Hackathon Requirement)
        </h2>
        <Card className="border-primary/20">
          <CardContent className="pt-6">
            <p className="text-muted-foreground mb-4">
              <strong className="text-primary">Thorax</strong> extensively uses <strong>SpoonOS components</strong> to meet the hackathon&apos;s technical requirements:
            </p>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">AI Agent Framework:</strong>
                  <p className="text-sm text-muted-foreground">
                    Utilizes SpoonOS&apos;s agent orchestration to create autonomous contract analysis agents that can reason about security risks,
                    interpret blockchain events, and make intelligent decisions about threat severity.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">LLM Integration:</strong>
                  <p className="text-sm text-muted-foreground">
                    Combines SpoonOS with Google Gemini for advanced natural language understanding of contract code,
                    generating human-readable security reports and legal analysis.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">Autonomous Decision Making:</strong>
                  <p className="text-sm text-muted-foreground">
                    AI agents autonomously monitor blockchain state, analyze events, and trigger alerts without human intervention,
                    demonstrating true agentic behavior.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Neo Blockchain Integration */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
          <Globe className="h-6 w-6 text-primary" />
          Neo Blockchain Integration
        </h2>
        <Card className="border-primary/20">
          <CardContent className="pt-6">
            <p className="text-muted-foreground mb-4">
              Built specifically for the <strong>Neo ecosystem</strong>, leveraging its unique features:
            </p>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">Neo RPC Integration:</strong>
                  <p className="text-sm text-muted-foreground">
                    Direct integration with Neo&apos;s RPC nodes for real-time blockchain data access, supporting both testnet and mainnet deployments.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">Contract Notification System:</strong>
                  <p className="text-sm text-muted-foreground">
                    Monitors Neo&apos;s native notification system to capture contract events with deterministic finality and low latency.
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-foreground">Multi-Language Support:</strong>
                  <p className="text-sm text-muted-foreground">
                    Compatible with Neo contracts written in C#, Python, and other supported languages through ABI analysis.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Use Cases */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
          <Lock className="h-6 w-6 text-primary" />
          Real-World Use Cases
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">DeFi Protocol Security</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Monitor DeFi contracts for suspicious withdrawals, unusual liquidity changes, or unauthorized access attempts.
              Receive instant alerts when potential exploits are detected.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">NFT Marketplace Protection</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Track NFT contract events for fraudulent minting, unauthorized transfers, or pricing manipulation.
              Ensure marketplace integrity with AI-powered monitoring.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">DAO Governance Oversight</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Monitor governance contracts for voting anomalies, proposal manipulation, or treasury access violations.
              Maintain transparency and security in decentralized organizations.
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">Token Contract Auditing</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Continuously audit token contracts for mint/burn events, supply changes, and ownership transfers.
              Detect potential rug pulls or malicious contract upgrades.
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Getting Started */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Getting Started</h2>
        <div className="space-y-4">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
              1
            </div>
            <div>
              <h3 className="font-semibold mb-1">Register Your Contract</h3>
              <p className="text-sm text-muted-foreground">
                Navigate to the Dashboard and enter your contract hash, select the network (testnet/mainnet), and provide your email for notifications.
                Optionally paste the contract ABI for enhanced analysis.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
              2
            </div>
            <div>
              <h3 className="font-semibold mb-1">Review AI Analysis</h3>
              <p className="text-sm text-muted-foreground">
                Once registered, view the comprehensive risk assessment including risk level (0-100%), identified breach vectors,
                monitoring events, and legal compliance analysis.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
              3
            </div>
            <div>
              <h3 className="font-semibold mb-1">Activate Monitoring</h3>
              <p className="text-sm text-muted-foreground">
                Click &quot;Activate&quot; to enable real-time monitoring. The system will continuously scan the blockchain for your contract&apos;s events
                and analyze them for security threats.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
              4
            </div>
            <div>
              <h3 className="font-semibold mb-1">Monitor & Respond</h3>
              <p className="text-sm text-muted-foreground">
                View detected events in the Events panel, filtered by time range (1 week, 1 month, 3 months).
                Receive email alerts for critical events and follow AI-recommended actions to secure your contract.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">Frontend</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-1">
              <p>• Next.js 16 (React 19)</p>
              <p>• TypeScript</p>
              <p>• Tailwind CSS</p>
              <p>• shadcn/ui Components</p>
              <p>• Lucide Icons</p>
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">Backend</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-1">
              <p>• FastAPI (Python)</p>
              <p>• Prisma ORM</p>
              <p>• PostgreSQL</p>
              <p>• Neo3-Python SDK</p>
              <p>• Web3.py (EVM support)</p>
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg">AI & Services</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-1">
              <p>• SpoonOS AI Agents</p>
              <p>• Google Gemini LLM</p>
              <p>• ElevenLabs Voice AI</p>
              <p>• SMTP Email Service</p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Hackathon Alignment */}
      <section className="mb-12 bg-primary/5 border border-primary/20 rounded-lg p-6">
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          Hackathon Track Alignment
        </h2>
        <p className="text-muted-foreground mb-4">
          <strong className="text-primary">Thorax</strong> is designed for the <strong>&quot;AI Agent with Web3&quot;</strong> track, demonstrating:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold mb-2 text-primary">✓ Autonomy</h3>
            <p className="text-sm text-muted-foreground">
              AI agents independently monitor blockchain state, analyze events, and trigger alerts without manual intervention.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2 text-primary">✓ Security</h3>
            <p className="text-sm text-muted-foreground">
              Implements safeguards including risk scoring, severity classification, and human-readable explanations for all AI decisions.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2 text-primary">✓ Usefulness</h3>
            <p className="text-sm text-muted-foreground">
              Solves real security challenges in Web3 by providing automated contract monitoring and threat detection.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2 text-primary">✓ Neo Integration</h3>
            <p className="text-sm text-muted-foreground">
              Built specifically for Neo blockchain with native RPC integration, contract notification monitoring, and multi-network support.
            </p>
          </div>
        </div>
      </section>

      {/* Limitations */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Current Limitations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="border-orange-500/20 bg-orange-500/5">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Lock className="h-5 w-5 text-orange-500" />
                Read-Only Design
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Agent monitors but does not execute on-chain transactions. Cannot automatically pause contracts or withdraw funds.
              <strong className="block mt-2 text-foreground">Why:</strong> Security-first approach prevents agent exploitation.
            </CardContent>
          </Card>

          <Card className="border-orange-500/20 bg-orange-500/5">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Globe className="h-5 w-5 text-orange-500" />
                Single Blockchain
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Currently supports Neo blockchain only. No cross-chain monitoring capabilities.
              <strong className="block mt-2 text-foreground">Why:</strong> Deep Neo integration over shallow multi-chain support.
            </CardContent>
          </Card>

          <Card className="border-orange-500/20 bg-orange-500/5">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Activity className="h-5 w-5 text-orange-500" />
                Reactive Detection
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Detects breaches after events occur. No predictive analytics for pre-exploit warnings.
              <strong className="block mt-2 text-foreground">Why:</strong> Hackathon timeline prioritized core functionality.
            </CardContent>
          </Card>

          <Card className="border-orange-500/20 bg-orange-500/5">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Bell className="h-5 w-5 text-orange-500" />
                Manual Registration
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Users must manually register each contract. No automatic discovery of related contracts.
              <strong className="block mt-2 text-foreground">Why:</strong> Explicit opt-in ensures user control and privacy.
            </CardContent>
          </Card>
        </div>
        <div className="mt-6 p-4 rounded-lg bg-muted/50 border border-border">
          <p className="text-sm text-muted-foreground">
            <strong className="text-foreground">Note:</strong> These limitations are intentional design choices that prioritize security,
            deep integration, and production readiness over feature breadth. The extensible architecture allows for future enhancements
            while maintaining a stable, secure core.
          </p>
        </div>
      </section>

      {/* Future Enhancements */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Future Enhancements</h2>

        <div className="space-y-6">
          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">Phase 1: Enhanced Automation (Q1 2025)</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• <strong>Automated Response Actions:</strong> Execute pre-signed emergency transactions to pause contracts or withdraw funds</li>
              <li>• <strong>Multi-Sig Integration:</strong> Coordinate with multi-signature wallets for emergency fund protection</li>
              <li>• <strong>Smart Response Playbooks:</strong> Configurable automated responses based on breach severity</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">Phase 2: Advanced AI (Q2 2025)</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• <strong>Predictive Analytics:</strong> Machine learning models to predict exploits before they happen</li>
              <li>• <strong>Pattern Recognition:</strong> Cross-contract analysis to identify emerging attack patterns</li>
              <li>• <strong>Collaborative Learning:</strong> Shared intelligence across agent instances for improved accuracy</li>
              <li>• <strong>Reduced False Positives:</strong> Continuous learning from user feedback</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">Phase 3: Multi-Chain Expansion (Q3 2025)</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• <strong>Ethereum & L2s:</strong> Support for Ethereum, Arbitrum, Optimism, Base</li>
              <li>• <strong>EVM Chains:</strong> Polygon, BSC, Avalanche integration</li>
              <li>• <strong>Cross-Chain Detection:</strong> Monitor bridge exploits and cross-chain attacks</li>
              <li>• <strong>Unified Dashboard:</strong> Single interface for all blockchain monitoring</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">Phase 4: Ecosystem Integration (Q4 2025)</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• <strong>Neo Oracle Integration:</strong> Leverage Neo&apos;s native oracles for real-world data</li>
              <li>• <strong>DeFi Protocol Integration:</strong> Direct monitoring of DEXs, lending protocols, yield aggregators</li>
              <li>• <strong>Mobile Apps:</strong> iOS/Android applications with push notifications</li>
              <li>• <strong>Community Threat Intelligence:</strong> Shared database of attack patterns and malicious contracts</li>
            </ul>
          </div>

          <div className="border-l-4 border-primary pl-6 py-2">
            <h3 className="text-xl font-semibold mb-2">Phase 5: Enterprise Features (2026)</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• <strong>White-Label Solutions:</strong> Customizable branding for protocols and enterprises</li>
              <li>• <strong>Insurance Integration:</strong> Automated claims filing and risk-based premium calculations</li>
              <li>• <strong>Advanced Analytics:</strong> Comprehensive dashboards with historical trends and benchmarking</li>
              <li>• <strong>API & Webhooks:</strong> Third-party integrations and real-time event streaming</li>
            </ul>
          </div>
        </div>

        <div className="mt-6 p-6 rounded-lg bg-primary/5 border border-primary/20">
          <h3 className="font-semibold mb-2 text-primary">Why This Roadmap Matters</h3>
          <p className="text-sm text-muted-foreground">
            This phased approach demonstrates our commitment to continuous improvement while maintaining security and stability.
            Each phase builds on the previous one, ensuring that new features integrate seamlessly with the existing architecture.
            The roadmap addresses current limitations systematically while expanding capabilities to serve a broader Web3 ecosystem.
          </p>
        </div>
      </section>
    </div>
  );
}
