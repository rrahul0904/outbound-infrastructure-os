import { ArrowRight, PauseCircle, Plus, Send, Sparkles } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { demoCampaigns } from "@/lib/demo";

export default function CampaignsPage() {
  return <AppShell active="Campaigns">
    <header className="topbar"><div><p className="eyebrow">OUTREACH / CAMPAIGNS</p><h1>Campaigns</h1><p>Build sequences against policy-approved sender capacity.</p></div><button className="primaryBtn"><Plus size={15}/> New campaign</button></header>
    <section className="metricGrid threeMetrics"><article className="metricCard"><div className="metricTop"><span>Active</span><Send size={17}/></div><strong>12</strong><small>8 healthy · 4 constrained</small></article><article className="metricCard"><div className="metricTop"><span>Queued recipients</span><ArrowRight size={17}/></div><strong>31,804</strong><small>Capacity checked before dispatch</small></article><article className="metricCard"><div className="metricTop"><span>AI-assisted drafts</span><Sparkles size={17}/></div><strong>18</strong><small>Human approval required</small></article></section>
    <article className="panel"><div className="panelHead"><div><h2>Campaign inventory</h2><p>Current workload, policy mode and response performance.</p></div></div><div className="tableWrap"><table><thead><tr><th>Campaign</th><th>Status</th><th>Contacts</th><th>Sent</th><th>Reply rate</th><th>Policy</th></tr></thead><tbody>{demoCampaigns.map(c=><tr key={c.name}><td><b>{c.name}</b></td><td><span className={`status ${c.status === "Active" ? "healthy" : c.status === "Paused" ? "attention" : "warming"}`}>{c.status}</span></td><td>{c.contacts}</td><td>{c.sent}</td><td>{c.reply}</td><td>{c.policy}</td></tr>)}</tbody></table></div></article>
    <div className="workflowStrip"><div><b>Sequence safety</b><span>Suppression → verification → schedule → sender health → capacity → dispatch</span></div><PauseCircle size={20}/><p>A campaign cannot bypass workspace suppression or sender-health policy.</p></div>
  </AppShell>;
}
