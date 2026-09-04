import { Bot, Mail, Reply, Search } from "lucide-react";
import { AppShell } from "@/components/AppShell";

const threads=[
  {sender:"Maya Chen",subject:"Re: Infrastructure consolidation",label:"Interested",preview:"Yes, this is timely. Can you send over a short architecture overview?",time:"10:42"},
  {sender:"Jon Bell",subject:"Re: Data platform operating model",label:"Question",preview:"How does this integrate with our existing CRM workflow?",time:"09:18"},
  {sender:"Priya Raman",subject:"Automatic reply",label:"Out of office",preview:"I am away until September 8. For urgent items contact…",time:"Yesterday"},
];

export default function InboxPage(){return <AppShell active="Master inbox">
  <header className="topbar"><div><p className="eyebrow">REPLIES / MASTER INBOX</p><h1>Master inbox</h1><p>One reply surface across managed sending identities.</p></div><button className="secondaryBtn"><Search size={15}/> Search replies</button></header>
  <section className="twoCol inboxGrid"><article className="panel"><div className="panelHead"><div><h2>Needs attention</h2><p>AI classification is advisory; humans control replies.</p></div></div><div className="threadList">{threads.map(t=><div className="thread" key={t.sender}><div className="threadAvatar">{t.sender.split(" ").map(x=>x[0]).join("")}</div><div><div className="threadTop"><b>{t.sender}</b><span>{t.time}</span></div><strong>{t.subject}</strong><p>{t.preview}</p><span className="threadLabel">{t.label}</span></div></div>)}</div></article>
  <article className="panel replyPreview"><div className="replyHero"><Mail size={22}/><div><p className="eyebrow">SELECTED CONVERSATION</p><h2>Maya Chen</h2><span>maya.chen@example.com</span></div></div><div className="messageBubble">Yes, this is timely. Can you send over a short architecture overview?</div><div className="aiSuggestion"><Bot size={17}/><div><b>Suggested intent</b><p>Interested · requested collateral. Suggested reply remains draft-only until approved.</p></div></div><button className="primaryBtn"><Reply size={15}/> Draft reply</button></article></section>
  </AppShell>}
