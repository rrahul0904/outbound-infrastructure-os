import { FileUp, ListFilter, Plus, ShieldCheck } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { demoContacts } from "@/lib/demo";

export default function ContactsPage() {
  return <AppShell active="Contacts">
    <header className="topbar"><div><p className="eyebrow">AUDIENCE / CONTACTS</p><h1>Contacts & lists</h1><p>Verification and suppression status stay attached to every prospect.</p></div><div className="topActions"><button className="secondaryBtn"><FileUp size={15}/> Import CSV</button><button className="primaryBtn"><Plus size={15}/> Add contact</button></div></header>
    <section className="metricGrid"><article className="metricCard"><div className="metricTop"><span>Total contacts</span><ListFilter size={17}/></div><strong>84,291</strong><small>Across 18 workspace lists</small></article><article className="metricCard good"><div className="metricTop"><span>Verified usable</span><ShieldCheck size={17}/></div><strong>96.7%</strong><small>81,510 eligible after policy</small></article><article className="metricCard"><div className="metricTop"><span>Risky</span><span>!</span></div><strong>1,108</strong><small>Not automatically eligible</small></article><article className="metricCard"><div className="metricTop"><span>Suppressed</span><span>×</span></div><strong>1,673</strong><small>Unsubscribe, complaint or hard bounce</small></article></section>
    <article className="panel"><div className="panelHead"><div><h2>Recent contacts</h2><p>Workspace-scoped inventory with verification posture.</p></div><button className="textBtn">Manage lists</button></div><div className="tableWrap"><table><thead><tr><th>Contact</th><th>Email</th><th>Company</th><th>Verification</th><th>List</th></tr></thead><tbody>{demoContacts.map(c=><tr key={c.email}><td><b>{c.name}</b></td><td>{c.email}</td><td>{c.company}</td><td><span className={`status ${c.verification === "Valid" ? "healthy" : "warming"}`}>{c.verification}</span></td><td>{c.list}</td></tr>)}</tbody></table></div></article>
  </AppShell>;
}
