"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export function Logs() {
  const [logs, setLogs] = useState<any[]>([]);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const es = new EventSource(`${BASE}/logs/stream`);
    esRef.current = es;
    es.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        setLogs((prev) => [...prev.slice(-99), data]);
      } catch {}
    };
    es.onerror = () => {
      es.close();
      esRef.current = null;
    };
    return () => {
      es.close();
      esRef.current = null;
    };
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Real-Time Logs</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 overflow-auto rounded border bg-background p-2 text-xs">
          {logs.length === 0 ? (
            <div className="text-muted-foreground">No logs yet...</div>
          ) : (
            logs.map((l, idx) => (
              <div key={idx} className="mb-1">
                <span className="font-medium">{l.type}</span>
                {l.event_name && <span> · {l.event_name}</span>}
                {typeof l.active !== "undefined" && <span> · active={String(l.active)}</span>}
                {l.network && <span> · net={l.network}</span>}
                {l.block && <span> · blk={l.block}</span>}
                {l.txid && <span> · tx={l.txid}</span>}
                {typeof l.breach_detected !== "undefined" && (
                  <span> · breach={String(l.breach_detected)}</span>
                )}
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}

