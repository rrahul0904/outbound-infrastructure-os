import Link from "next/link";
import { Activity, AtSign, BarChart3, Blocks, Inbox, LayoutDashboard, Megaphone, Settings2, ShieldCheck, UsersRound } from "lucide-react";

const sections = [
  { label: "Overview", href: "/", icon: LayoutDashboard },
  { label: "Campaigns", href: "/campaigns", icon: Megaphone },
  { label: "Contacts", href: "/contacts", icon: UsersRound },
  { label: "Master inbox", href: "/inbox", icon: Inbox },
  { label: "Domains", href: "/domains", icon: AtSign },
  { label: "Reputation", href: "/reputation", icon: Activity },
  { label: "Blocklists", href: "/blocklists", icon: ShieldCheck },
  { label: "Analytics", href: "/analytics", icon: BarChart3 },
  { label: "Integrations", href: "/integrations", icon: Blocks },
];

export function Sidebar({ active }: { active: string }) {
  return (
    <aside className="sidebar">
      <div className="brandMark"><span>O</span><strong>OutboundOS</strong></div>
      <div className="workspace"><div className="workspaceAvatar">AC</div><div><b>Acme GTM</b><small>Production workspace</small></div></div>
      <nav>{sections.map(({ label, href, icon: Icon }) => <Link className={active === label ? "navItem active" : "navItem"} href={href} key={label}><Icon size={17}/><span>{label}</span></Link>)}</nav>
      <div className="sidebarBottom"><a className="navItem" href="#"><Settings2 size={17}/><span>Settings</span></a><div className="userCard"><div className="userAvatar">RS</div><div><b>Workspace owner</b><small>Administrator</small></div></div></div>
    </aside>
  );
}
