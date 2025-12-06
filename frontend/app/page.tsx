/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-hooks/set-state-in-effect */
"use client";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { toast } from "sonner";
import { Logs } from "@/components/Logs";
import { Shield, Activity, FileText, Play, RefreshCw, Eye, AlertTriangle, Trash2, Bell, CheckCircle2, XCircle } from "lucide-react";

const BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [contracts, setContracts] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [selectedContract, setSelectedContract] = useState<string>("");
  const [rangePreset, setRangePreset] = useState<string>("");
  const [loadingEvents, setLoadingEvents] = useState<boolean>(false);
  const [registerForm, setRegisterForm] = useState({ contract_hash: "", abi: "", raw_tx_hex: "", network: "testnet", chain: "neo", owner_email: "" });
  const [registerResult, setRegisterResult] = useState<any>(null);
  const [registerLoading, setRegisterLoading] = useState<boolean>(false);
  const [formErrors, setFormErrors] = useState<{[key: string]: string}>({});
  const [legalAbi, setLegalAbi] = useState<string>("{\n  \"methods\": [{\"name\": \"rescueFunds\"}]\n}");
  const [legalVoice, setLegalVoice] = useState<boolean>(false);
  const [legalResult, setLegalResult] = useState<any>(null);
  const [abiRiskResult, setAbiRiskResult] = useState<any>(null);
  const [rawTx, setRawTx] = useState<string>("");
  const [exitResult, setExitResult] = useState<any>(null);
  const [analysisOpenId, setAnalysisOpenId] = useState<string>("");
  const openAnalysis = (id: string) => setAnalysisOpenId(id);
  const closeAnalysis = () => setAnalysisOpenId("");
  const [deletingId, setDeletingId] = useState<string>("");
  const [alertOpenId, setAlertOpenId] = useState<string>("");
  const [alertMessage, setAlertMessage] = useState<string>("");
  const [alertVoice, setAlertVoice] = useState<boolean>(true);
// n
  const fetchContracts = async () => {
    const r = await fetch(`${BASE}/contracts`);
    const j = await r.json();
    setContracts(j.contracts || []);
  };
  const fetchEvents = async () => {
    setLoadingEvents(true);
    try {
      if (selectedContract) {
        const params = new URLSearchParams();
        if (rangePreset) params.set("range", rangePreset);
        const r = await fetch(`${BASE}/contracts/${selectedContract}/events?${params.toString()}`);
        const j = await r.json();
        setEvents(j.events || []);
      } else {
        const r = await fetch(`${BASE}/events`);
        const j = await r.json();
        setEvents(j.events || []);
      }
    } finally {
      setLoadingEvents(false);
    }
  };

  const short = (s: string | undefined) => {
    if (!s) return "";
    return s.length > 12 ? `${s.slice(0, 6)}...${s.slice(-4)}` : s;
  };
  const fetchHealth = async () => {
    const r = await fetch(`${BASE}/health/detail`);
    const j = await r.json();
    setHealth(j);
  };
  const fetchMetrics = async () => {
    const r = await fetch(`${BASE}/metrics`);
    const j = await r.json();
    setMetrics(j.metrics || {});
  };
  useEffect(() => {
    setTimeout(() => {
      fetchHealth();
      fetchMetrics();
      fetchContracts();
      fetchEvents();
    }, 0);
  }, []);

  const validateForm = () => {
    const errors: {[key: string]: string} = {};

    if (!registerForm.contract_hash.trim()) {
      errors.contract_hash = "Contract hash is required";
    }

    if (!registerForm.owner_email.trim()) {
      errors.owner_email = "Owner email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.owner_email)) {
      errors.owner_email = "Please enter a valid email address";
    }

    if (registerForm.abi && registerForm.abi.trim()) {
      try {
        JSON.parse(registerForm.abi);
      } catch {
        errors.abi = "ABI must be valid JSON";
      }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const registerContract = async () => {
    if (!validateForm()) {
      toast.error("Please fix the form errors before submitting");
      return;
    }

    try {
      setRegisterLoading(true);
      setFormErrors({});
      const body: any = { network: registerForm.network, chain: registerForm.chain, owner_email: registerForm.owner_email };
      if (registerForm.contract_hash) body.contract_hash = registerForm.contract_hash;
      if (registerForm.abi) { try { body.abi = JSON.parse(registerForm.abi); } catch {} }
      if (registerForm.raw_tx_hex) body.raw_tx_hex = registerForm.raw_tx_hex;
      const r = await fetch(`${BASE}/register-contract`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const j = await r.json();
      setRegisterResult(j);
      fetchContracts();
      toast.success("Contract registered successfully");
    } catch (error) {
      toast.error("Failed to register contract");
    } finally {
      setRegisterLoading(false);
    }
  };
  const [activatingId, setActivatingId] = useState<string>("");
  const toggleActive = async (id: string, active: boolean) => {
    try {
      setActivatingId(id);
      await fetch(`${BASE}/contracts/${id}/activate`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ active }) });
      fetchContracts();
      toast.success(`Contract ${active ? "activated" : "deactivated"} successfully`);
    } catch (error) {
      toast.error("Failed to update contract status");
    } finally {
      setActivatingId("");
    }
  };
  const [monitoring, setMonitoring] = useState<boolean>(false);
  const monitorOnce = async () => {
    try {
      setMonitoring(true);
      const r = await fetch(`${BASE}/monitor-once`, { method: "POST" });
      const j = await r.json();
      fetchMetrics();
      fetchEvents();
      toast.success("Monitoring completed successfully");
    } catch (error) {
      toast.error("Monitoring failed");
    } finally {
      setMonitoring(false);
    }
  };
  const analyzeLegal = async () => {
    let abiObj: any = {};
    try {
      abiObj = JSON.parse(legalAbi);
    } catch {}
    try {
      const r = await fetch(`${BASE}/legal-analyze`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ abi: abiObj, voice: legalVoice }) });
      const j = await r.json();
      setLegalResult(j);
      toast.success("Legal analysis completed");
    } catch (error) {
      toast.error("Legal analysis failed");
    }
  };
  const analyzeAbiRisk = async () => {
    let abiObj: any = {};
    try {
      abiObj = JSON.parse(legalAbi);
    } catch {}
    try {
      const r = await fetch(`${BASE}/analyze-abi`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ abi: abiObj }) });
      const j = await r.json();
      setAbiRiskResult(j.analysis);
      toast.success("ABI risk analysis completed");
    } catch (error) {
      toast.error("ABI risk analysis failed");
    }
  };
  const exitBroadcast = async () => {
    try {
      const r = await fetch(`${BASE}/exit`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ raw_tx_hex: rawTx }) });
      const j = await r.json();
      setExitResult(j);
      toast.success("Exit broadcast completed");
    } catch (error) {
      toast.error("Exit broadcast failed");
    }
  };

  const deleteContract = async (id: string) => {
    try {
      if (!confirm("Delete this contract and its events?")) return;
      setDeletingId(id);
      const r = await fetch(`${BASE}/contracts/${id}`, { method: "DELETE" });
      if (!r.ok) throw new Error("delete failed");
      await fetchContracts();
      toast.success("Contract deleted");
    } catch (e) {
      toast.error("Failed to delete contract");
    } finally {
      setDeletingId("");
    }
  };

  const sendAlert = async (id: string) => {
    try {
      const r = await fetch(`${BASE}/notify`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ contract_id: id, message: alertMessage || "Security notice", voice: alertVoice }) });
      const j = await r.json();
      if (!("sent" in j)) throw new Error("notify failed");
      toast.success("Alert sent");
      setAlertOpenId("");
      setAlertMessage("");
    } catch (e) {
      toast.error("Failed to send alert");
    }
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen w-full bg-background text-foreground">
        <div className="mx-auto max-w-6xl px-6 py-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="relative">
              <div className="absolute inset-0 bg-primary/10 blur-lg rounded-full"></div>
              <Shield className="h-10 w-10 text-primary relative" />
            </div>
            <h1 className="text-4xl font-bold tracking-tight">
              Thorax Dashboard
            </h1>
          </div>
          <p className="text-muted-foreground mb-6">AI-Powered Smart Contract Monitoring for Neo Blockchain</p>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-sm font-medium">
                <Activity className="h-4 w-4 text-primary" />
                System Health
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                  <div className="flex items-center gap-2">
                    <div className={`h-2 w-2 rounded-full ${health?.spoon_available ? "bg-green-500 animate-pulse" : "bg-red-500"}`}></div>
                    <span className="text-sm font-medium">SpoonOS</span>
                  </div>
                  <span className={`text-sm font-semibold ${health?.spoon_available ? "text-green-500" : "text-red-500"}`}>
                    {health?.spoon_available ? "Available" : "Unavailable"}
                  </span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                  <div className="flex items-center gap-2">
                    <div className={`h-2 w-2 rounded-full ${health?.gemini_configured ? "bg-green-500 animate-pulse" : "bg-red-500"}`}></div>
                    <span className="text-sm font-medium">Gemini AI</span>
                  </div>
                  <span className={`text-sm font-semibold ${health?.gemini_configured ? "text-green-500" : "text-red-500"}`}>
                    {health?.gemini_configured ? "Configured" : "Not Configured"}
                  </span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                  <div className="flex items-center gap-2">
                    <div className={`h-2 w-2 rounded-full ${health?.elevenlabs_configured ? "bg-green-500 animate-pulse" : "bg-red-500"}`}></div>
                    <span className="text-sm font-medium">ElevenLabs</span>
                  </div>
                  <span className={`text-sm font-semibold ${health?.elevenlabs_configured ? "text-green-500" : "text-red-500"}`}>
                    {health?.elevenlabs_configured ? "Configured" : "Not Configured"}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  Register Contract
                </CardTitle>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="ghost" size="sm">?</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Contract Registration Help</DialogTitle>
                      <DialogDescription>
                        Register smart contracts for monitoring and analysis.
                        
                        <div className="mt-4 space-y-2">
                          <p><strong>Contract Hash:</strong> The unique identifier of your smart contract on the blockchain.</p>
                          <p><strong>Network:</strong> Select whether your contract is deployed on testnet or mainnet.</p>
                          <p><strong>Owner Email:</strong> Email address for notifications about contract events and alerts.</p>
                        </div>
                        
                        <div className="mt-4">
                          <p className="text-sm text-muted-foreground">
                            Fill in all fields and click &quot;Register Contract&quot; to add your contract to the monitoring system.
                          </p>
                        </div>
                      </DialogDescription>
                    </DialogHeader>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <Input
                    placeholder="Contract Hash *"
                    value={registerForm.contract_hash}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, contract_hash: e.target.value });
                      if (formErrors.contract_hash) setFormErrors({ ...formErrors, contract_hash: "" });
                    }}
                    className={formErrors.contract_hash ? "border-red-500" : ""}
                  />
                  {formErrors.contract_hash && (
                    <p className="mt-1 text-xs text-red-500">{formErrors.contract_hash}</p>
                  )}
                </div>
                <select
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={registerForm.network}
                  onChange={(e) => setRegisterForm({ ...registerForm, network: e.target.value })}
                >
                  <option value="testnet">Testnet</option>
                  <option value="mainnet">Mainnet</option>
                </select>
                <select
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={registerForm.chain}
                  onChange={(e) => setRegisterForm({ ...registerForm, chain: e.target.value })}
                >
                  <option value="neo">Neo</option>
                  <option value="evm">EVM</option>
                </select>
                <div>
                  <Input
                    placeholder="Owner Email *"
                    type="email"
                    value={registerForm.owner_email}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, owner_email: e.target.value });
                      if (formErrors.owner_email) setFormErrors({ ...formErrors, owner_email: "" });
                    }}
                    className={formErrors.owner_email ? "border-red-500" : ""}
                  />
                  {formErrors.owner_email && (
                    <p className="mt-1 text-xs text-red-500">{formErrors.owner_email}</p>
                  )}
                </div>
                <div>
                  <textarea
                    className={`min-h-[100px] w-full rounded-md border ${formErrors.abi ? "border-red-500" : "border-input"} bg-background px-3 py-2 text-sm`}
                    placeholder="Paste ABI JSON (optional)"
                    value={registerForm.abi}
                    onChange={(e) => {
                      setRegisterForm({ ...registerForm, abi: e.target.value });
                      if (formErrors.abi) setFormErrors({ ...formErrors, abi: "" });
                    }}
                  />
                  {formErrors.abi && (
                    <p className="mt-1 text-xs text-red-500">{formErrors.abi}</p>
                  )}
                </div>
                <Input
                  placeholder="Raw TX Hex (optional)"
                  value={registerForm.raw_tx_hex}
                  onChange={(e) => setRegisterForm({ ...registerForm, raw_tx_hex: e.target.value })}
                />
                <Button onClick={registerContract} className="w-full" disabled={registerLoading}>{registerLoading ? "Registering..." : "Register Contract"}</Button>
                {registerResult && (
                  <div className="mt-3 text-sm space-y-1">
                    <div className="flex justify-between"><span>Risk Level:</span><span className={registerResult.analysis?.risk_level >= 7 ? "text-red-500" : registerResult.analysis?.risk_level >= 4 ? "text-yellow-500" : "text-green-500"}>{registerResult.analysis?.risk_level ?? 0}</span></div>
                    <div className="text-xs text-muted-foreground">
                      Events: {(registerResult.analysis?.monitoring_events || []).join(", ")}
                    </div>
                    {registerResult.analysis?.legal && (
                      <div className="text-xs">Legal: {registerResult.analysis.legal.recommendation}</div>
                    )}
                    {registerResult.exit_broadcast && (
                      <div className="text-xs">Exit: {registerResult.exit_broadcast.success ? "Submitted" : "Failed"}</div>
                    )}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Play className="h-5 w-5 text-primary" />
                  Controls
                </CardTitle>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="ghost" size="sm">?</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Controls Help</DialogTitle>
                      <DialogDescription>
                        <div className="space-y-2 text-sm">
                          <p><strong>Monitor Once:</strong> triggers one immediate scan across configured networks to ingest events.</p>
                          <p><strong>Refresh Contracts:</strong> reloads the contract list.</p>
                          <p><strong>Refresh Events:</strong> reloads events for the selected contract or all.</p>
                          <p><strong>View Events:</strong> shows events for a contract; use range presets for time windows.</p>
                          <p><strong>View Analysis:</strong> opens AI analysis including monitoring events and formatted report.</p>
                          <p><strong>Activate/Deactivate:</strong> toggles monitoring for a contract.</p>
                          <p><strong>Send Alert:</strong> manually emails the owner with optional voice synthesis.</p>
                          <p><strong>Delete:</strong> removes the contract and its events.</p>
                          <p><strong>Real-Time Logs:</strong> shows live activation and monitoring event logs.</p>
                        </div>
                      </DialogDescription>
                    </DialogHeader>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Button onClick={monitorOnce} variant="outline" className="w-full" disabled={monitoring}>
                  <Play className="h-4 w-4 mr-2" />
                  {monitoring ? "Monitoring..." : "Monitor Once"}
                </Button>
                <Button onClick={fetchContracts} variant="outline" className="w-full">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh Contracts
                </Button>
                <Button onClick={fetchEvents} variant="outline" className="w-full">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh Events
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-primary" />
                Contracts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                {contracts.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <Shield className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p>No contracts registered yet</p>
                    <p className="text-xs mt-1">Register a contract to start monitoring</p>
                  </div>
                ) : (
                  contracts.map((c) => (
                    <div key={c.id} className="flex flex-col gap-3 rounded-lg border p-3 bg-card">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex-1 min-w-0">
                          <div className="font-medium truncate" title={c.contract_name || c.contract_hash}>
                            {short(c.contract_name || c.contract_hash)}
                          </div>
                          <div className="text-sm text-muted-foreground flex flex-wrap gap-x-3 gap-y-1 mt-1">
                            <span className="flex items-center gap-1">
                              {c.active ? (
                                <CheckCircle2 className="h-3 w-3 text-green-500" />
                              ) : (
                                <XCircle className="h-3 w-3 text-gray-500" />
                              )}
                              {c.active ? "Active" : "Inactive"}
                            </span>
                            <span className={`font-medium ${
                              Math.round(((c.risk_level || 0) / 10) * 100) >= 70 ? "text-red-500" :
                              Math.round(((c.risk_level || 0) / 10) * 100) >= 40 ? "text-yellow-500" :
                              "text-green-500"
                            }`}>
                              Risk: {Math.round(((c.risk_level || 0) / 10) * 100)}%
                            </span>
                            <span>Chain: {c.chain || "neo"}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        <Button
                          variant={selectedContract === c.id ? "default" : "outline"}
                          size="sm"
                          onClick={() => { setSelectedContract(c.id); fetchEvents(); }}
                          className="flex-shrink-0"
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          Events
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => openAnalysis(c.id)}
                          className="flex-shrink-0"
                        >
                          <FileText className="h-4 w-4 mr-1" />
                          Analysis
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setAlertOpenId(c.id)}
                          className="flex-shrink-0"
                        >
                          <Bell className="h-4 w-4 mr-1" />
                          Alert
                        </Button>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant={c.active ? "destructive" : "default"}
                              size="sm"
                              onClick={() => toggleActive(c.id, !c.active)}
                              disabled={activatingId === c.id}
                              className="flex-shrink-0"
                            >
                              {c.active ? <XCircle className="h-4 w-4 mr-1" /> : <CheckCircle2 className="h-4 w-4 mr-1" />}
                              {activatingId === c.id ? (c.active ? "Deactivating..." : "Activating...") : (c.active ? "Deactivate" : "Activate")}
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>{c.active ? "Deactivate this contract" : "Activate this contract"}</p>
                          </TooltipContent>
                        </Tooltip>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => deleteContract(c.id)}
                          disabled={deletingId === c.id}
                          className="flex-shrink-0"
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          {deletingId === c.id ? "Deleting..." : "Delete"}
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-primary" />
                Events
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loadingEvents && (
                <div className="mb-2 text-xs flex items-center gap-2">
                  <RefreshCw className="h-3 w-3 animate-spin" />
                  Loading events...
                </div>
              )}
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <Button variant={rangePreset === "1w" ? "default" : "outline"} size="sm" onClick={() => { setRangePreset("1w"); fetchEvents(); }}>1 Week</Button>
                <Button variant={rangePreset === "1m" ? "default" : "outline"} size="sm" onClick={() => { setRangePreset("1m"); fetchEvents(); }}>1 Month</Button>
                <Button variant={rangePreset === "3m" ? "default" : "outline"} size="sm" onClick={() => { setRangePreset("3m"); fetchEvents(); }}>3 Months</Button>
                <Button variant="outline" size="sm" onClick={() => { setRangePreset(""); fetchEvents(); }}>All</Button>
              </div>
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                {events.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <AlertTriangle className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p>No events recorded yet</p>
                    <p className="text-xs mt-1">
                      {selectedContract ? "No events for this contract" : "Activate monitoring to start tracking events"}
                    </p>
                  </div>
                ) : (
                  events.map((e) => (
                    <div key={e.id} className="rounded-lg border p-3 bg-card">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="font-medium flex-1">{e.event_name}</div>
                        {e.breach_detected && (
                          <span className="px-2 py-0.5 text-xs font-medium bg-red-500/20 text-red-500 rounded-full">
                            Breach
                          </span>
                        )}
                      </div>
                      <div className="text-sm text-muted-foreground flex flex-wrap gap-x-3 gap-y-1">
                        <span className={`font-medium ${
                          e.severity === "critical" ? "text-red-500" :
                          e.severity === "high" ? "text-orange-500" :
                          e.severity === "medium" ? "text-yellow-500" :
                          "text-blue-500"
                        }`}>
                          Severity: {e.severity || "n/a"}
                        </span>
                        <span className="text-xs">
                          {e.timestamp ? new Date((e.timestamp as number) * 1000).toLocaleString() : "n/a"}
                        </span>
                      </div>
                      {e.recommended_action && (
                        <div className="mt-2 text-xs bg-primary/10 border border-primary/20 rounded p-2">
                          <strong className="text-primary">Recommended:</strong> {e.recommended_action}
                        </div>
                      )}
                      {e.raw_event && e.raw_event.ai_message && (
                        <div className="mt-2 text-xs bg-muted/50 rounded p-2">
                          <strong>AI Analysis:</strong> {e.raw_event.ai_message}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
        {analysisOpenId && (
          <Dialog open={true} onOpenChange={(v) => { if (!v) closeAnalysis(); }}>
            <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  Contract Analysis
                </DialogTitle>
                <DialogDescription>
                  Detailed AI analysis and monitoring configuration
                </DialogDescription>
              </DialogHeader>
              {(() => {
                const c = contracts.find((x) => x.id === analysisOpenId);
                if (!c) return <div className="text-sm">Contract not found</div>;
                const riskPercent = Math.round(((c.risk_level || 0) / 10) * 100);
                return (
                  <div className="space-y-4 text-sm">
                    <div className="grid grid-cols-2 gap-3">
                      <div className="p-3 rounded-lg bg-muted/50">
                        <div className="text-xs text-muted-foreground mb-1">Contract Name</div>
                        <div className="font-medium break-all">{c.contract_name || c.contract_hash}</div>
                      </div>
                      <div className="p-3 rounded-lg bg-muted/50">
                        <div className="text-xs text-muted-foreground mb-1">Risk Level</div>
                        <div className={`font-bold text-lg ${
                          riskPercent >= 70 ? "text-red-500" :
                          riskPercent >= 40 ? "text-yellow-500" :
                          "text-green-500"
                        }`}>
                          {riskPercent}%
                        </div>
                      </div>
                    </div>

                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="text-xs text-muted-foreground mb-2">Breach Vectors</div>
                      <div className="flex flex-wrap gap-2">
                        {(c.breach_vectors || []).length > 0 ? (
                          (c.breach_vectors || []).map((vector: string, idx: number) => (
                            <span key={idx} className="px-2 py-1 text-xs bg-red-500/20 text-red-500 rounded-md border border-red-500/30">
                              {vector}
                            </span>
                          ))
                        ) : (
                          <span className="text-muted-foreground">None identified</span>
                        )}
                      </div>
                    </div>

                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="text-xs text-muted-foreground mb-2">Monitoring Events</div>
                      <div className="flex flex-wrap gap-2">
                        {(c.monitoring_events || []).length > 0 ? (
                          (c.monitoring_events || []).map((event: string, idx: number) => (
                            <span key={idx} className="px-2 py-1 text-xs bg-primary/20 text-primary rounded-md border border-primary/30">
                              {event}
                            </span>
                          ))
                        ) : (
                          <span className="text-muted-foreground">None configured</span>
                        )}
                      </div>
                    </div>

                    <div>
                      <div className="text-xs text-muted-foreground mb-2 font-semibold">AI-Generated Report</div>
                      <pre className="max-h-64 overflow-auto whitespace-pre-wrap rounded-lg border bg-background p-3 text-xs leading-relaxed">
                        {c.formatted_report || "No report available"}
                      </pre>
                    </div>
                  </div>
                );
              })()}
            </DialogContent>
          </Dialog>
        )}
        {alertOpenId && (
          <Dialog open={true} onOpenChange={(v) => { if (!v) setAlertOpenId(""); }}>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Bell className="h-5 w-5 text-primary" />
                  Send Manual Alert
                </DialogTitle>
                <DialogDescription>
                  Send email notification (with optional AI voice synthesis) to the contract owner.
                </DialogDescription>
              </DialogHeader>
              {(() => {
                const contract = contracts.find((c) => c.id === alertOpenId);
                if (!contract) return <div className="text-sm text-muted-foreground">Contract not found</div>;

                return (
                  <div className="space-y-4">
                    <div className="p-3 rounded-lg bg-primary/10 border border-primary/20">
                      <div className="text-xs text-muted-foreground mb-1">Sending to:</div>
                      <div className="font-medium text-sm flex items-center gap-2">
                        <span className="text-primary">📧</span>
                        {contract.owner_email || "No email configured"}
                      </div>
                      <div className="text-xs text-muted-foreground mt-1">
                        Contract: {short(contract.contract_name || contract.contract_hash)}
                      </div>
                    </div>

                    <div>
                      <label className="text-sm font-medium mb-2 block">Alert Message</label>
                      <textarea
                        className="min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/50"
                        placeholder="Enter your alert message here..."
                        value={alertMessage}
                        onChange={(e) => setAlertMessage(e.target.value)}
                      />
                      <p className="text-xs text-muted-foreground mt-1">
                        This message will be sent to the contract owner&apos;s email address above.
                      </p>
                    </div>

                    <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                      <input
                        type="checkbox"
                        id="voice-toggle"
                        checked={alertVoice}
                        onChange={(e) => setAlertVoice(e.target.checked)}
                        className="h-4 w-4 rounded border-input"
                      />
                      <label htmlFor="voice-toggle" className="text-sm flex-1 cursor-pointer">
                        <div className="font-medium">Include AI Voice Synthesis</div>
                        <div className="text-xs text-muted-foreground">Generate audio version via ElevenLabs</div>
                      </label>
                    </div>

                    <div className="flex gap-2 pt-2">
                      <Button
                        onClick={() => sendAlert(alertOpenId)}
                        className="flex-1"
                        disabled={!alertMessage.trim() || !contract.owner_email}
                      >
                        <Bell className="h-4 w-4 mr-2" />
                        Send Alert
                      </Button>
                      <Button variant="outline" onClick={() => setAlertOpenId("")}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                );
              })()}
            </DialogContent>
          </Dialog>
        )}
        <div className="mt-6">
          <Logs />
        </div>
        {/* Removed Legal Analysis and Exit Broadcast cards as requested */}
      </div>
    </div>
    </TooltipProvider>
  );
}
