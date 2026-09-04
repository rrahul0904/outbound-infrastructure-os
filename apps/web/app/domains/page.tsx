import { Activity, Plus, ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { demoDomains } from "@/lib/demo";

export default function DomainsPage() {
  return <AppShell active="Domains">
    <header className="topbar"><div><p className="eyebrow">INFRASTRUCTURE / DOMAINS</p><h1>Sending domains</h1><p>DNS posture, warmup state and policy-approved daily capacity.</p></div><button className="primaryBtn"><Plus size={15}/> Add domain</button></header>
    <div className="notice"><ShieldCheck size={18}/><div><strong>Ownership and DNS readiness are server enforced.</strong><span> Campaigns can allocate only capacity from domains in an eligible state.</span></div></div>
    <article className="panel"><div className="panelHead"><div><h2>Domain registry</h2><p>State-machine status is separated from raw health score.</p></div></div><div className="tableWrap"><table><thead><tr><th>Domain</th><th>State</th><th>Health</th><th>Daily use</th><th>DNS</th><th>Warmup</th></tr></thead><tbody>{demoDomains.map(d=><tr key={d.domain}><td><b>{d.domain}</b></td><td><span className={`status ${d.state === "Ready" ? "healthy" : d.state === "Degraded" ? "attention" : "warming"}`}>{d.state}</span></td><td><div className="healthCell"><Activity size={14}/>{d.health}</div></td><td>{d.daily}</td><td>{d.dns}</td><td>{d.warmup}</td></tr>)}</tbody></table></div></article>
  </AppShell>;
}
