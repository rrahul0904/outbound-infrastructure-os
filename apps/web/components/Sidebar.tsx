import { Activity, AtSign, BarChart3, Blocks, Inbox, LayoutDashboard, Megaphone, Settings2, ShieldCheck, UsersRound } from "lucide-react";

const sections = [
  { label: "Overview", icon: LayoutDashboard, active: true },
  { label: "Campaigns", icon: Megaphone },
  { label: "Contacts", icon: UsersRound },
  { label: "Master inbox", icon: Inbox },
  { label: "Domains", icon: AtSign },
  { label: "Reputation", icon: Activity },
  { label: "Blocklists", icon: ShieldCheck },
  { label: "Analytics", icon: BarChart3 },
  { label: "Integrations", icon: Blocks },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brandMark"><span>O</span><strong>OutboundOS</strong></div>
      <div className="workspace"><div className="workspaceAvatar">AC</div><div><b>Acme GTM</b><small>Production workspace</small></div></div>
      <nav>
        {sections.map(({ label, icon: Icon, active }) => (
          <a className={active ? "navItem active" : "navItem"} href="#" key={label}><Icon size={17}/><span>{label}</span></a>
        ))}
      </nav>
      <div className="sidebarBottom">
        <a className="navItem" href="#"><Settings2 size={17}/><span>Settings</span></a>
        <div className="userCard"><div className="userAvatar">RS</div><div><b>Workspace owner</b><small>Administrator</small></div></div>
      </div>
    </aside>
  );
}
