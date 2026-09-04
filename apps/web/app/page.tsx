import { Activity, AlertTriangle, ArrowRight, CheckCircle2, CircleGauge, MailCheck, Send, Server, ShieldCheck } from "lucide-react";
import { Sidebar } from "@/components/Sidebar";
import { MetricCard } from "@/components/MetricCard";

const domains = [
  { domain: "reach.acme.example", status: "Healthy", health: 98, sent: "1,482", bounce: "0.8%", capacity: "72%" },
  { domain: "hello.acme.example", status: "Warming", health: 84, sent: "642", bounce: "1.1%", capacity: "38%" },
  { domain: "connect.acme.example", status: "Attention", health: 69, sent: "518", bounce: "3.9%", capacity: "22%" },
];

const events = [
  { type: "good", title: "SPF and DKIM verified", detail: "reach.acme.example · 8 minutes ago" },
  { type: "warn", title: "Bounce threshold crossed", detail: "connect.acme.example · sending automatically throttled" },
  { type: "good", title: "2,400 contacts verified", detail: "Enterprise SaaS Q3 list · 41 invalid addresses suppressed" },
  { type: "info", title: "Campaign capacity rebalanced", detail: "312 queued recipients moved to healthy sender capacity" },
];

export default function HomePage() {
  return (
    <main className="appShell">
      <Sidebar />
      <section className="content">
        <header className="topbar"><div><p className="eyebrow">CONTROL PLANE / OVERVIEW</p><h1>Infrastructure overview</h1><p>Sender health, capacity and campaign operations in one place.</p></div><div className="topActions"><button className="secondaryBtn">View incidents</button><button className="primaryBtn">Add sending domain <ArrowRight size={16}/></button></div></header>

        <div className="notice"><ShieldCheck size={18}/><div><strong>Policy engine is protecting sender reputation.</strong><span> 1 domain was automatically throttled after a bounce-rate anomaly.</span></div><button>Review action</button></div>

        <section className="metricGrid">
          <MetricCard label="Domains ready" value="18 / 22" helper="3 warming · 1 attention" icon={Server} tone="good" />
          <MetricCard label="Messages today" value="8,742" helper="63% of safe daily capacity" icon={Send} />
          <MetricCard label="Delivery rate" value="97.8%" helper="+0.6% versus 7-day average" icon={MailCheck} tone="good" />
          <MetricCard label="Positive replies" value="6.4%" helper="121 interested conversations" icon={Activity} />
        </section>

        <section className="twoCol">
          <article className="panel">
            <div className="panelHead"><div><h2>Sending infrastructure</h2><p>Highest-risk domains are surfaced first.</p></div><button className="textBtn">View all domains</button></div>
            <div className="tableWrap"><table><thead><tr><th>Domain</th><th>Status</th><th>Health</th><th>Sent today</th><th>Bounce</th><th>Capacity</th></tr></thead><tbody>{domains.map((d) => <tr key={d.domain}><td><b>{d.domain}</b></td><td><span className={`status ${d.status.toLowerCase()}`}>{d.status}</span></td><td><div className="healthCell"><CircleGauge size={15}/><span>{d.health}</span></div></td><td>{d.sent}</td><td className={d.bounce === "3.9%" ? "dangerText" : ""}>{d.bounce}</td><td><div className="capacity"><span style={{width:d.capacity}}></span></div><small>{d.capacity}</small></td></tr>)}</tbody></table></div>
          </article>

          <article className="panel activityPanel">
            <div className="panelHead"><div><h2>Operational events</h2><p>Automated actions and infrastructure changes.</p></div></div>
            <div className="eventList">{events.map((e) => <div className="event" key={e.title}><div className={`eventIcon ${e.type}`}>{e.type === "warn" ? <AlertTriangle size={16}/> : e.type === "good" ? <CheckCircle2 size={16}/> : <Activity size={16}/>}</div><div><b>{e.title}</b><p>{e.detail}</p></div></div>)}</div>
          </article>
        </section>

        <section className="threeCol">
          <article className="panel compact"><div className="panelHead"><div><h2>Campaign pipeline</h2><p>Current sending workload</p></div></div><div className="statRows"><div><span>Active campaigns</span><b>12</b></div><div><span>Queued recipients</span><b>31,804</b></div><div><span>Replies awaiting review</span><b>47</b></div><div><span>Safe capacity remaining</span><b>12,910</b></div></div></article>
          <article className="panel compact"><div className="panelHead"><div><h2>Reputation posture</h2><p>Cross-domain health</p></div></div><div className="score"><strong>92</strong><span>/100</span></div><div className="scoreBar"><span></span></div><p className="muted">No critical blacklist events. Complaint and unsubscribe rates remain within policy.</p></article>
          <article className="panel compact"><div className="panelHead"><div><h2>Verification</h2><p>Contact quality today</p></div></div><div className="verificationRing"><div><strong>96.7%</strong><span>usable</span></div></div><div className="miniLegend"><span><i className="dot goodDot"></i> Valid 8,942</span><span><i className="dot warnDot"></i> Risky 181</span><span><i className="dot badDot"></i> Suppressed 126</span></div></article>
        </section>
      </section>
    </main>
  );
}
