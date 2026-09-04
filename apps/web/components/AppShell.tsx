import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";

export function AppShell({ active, children }: { active: string; children: ReactNode }) {
  return <main className="appShell"><Sidebar active={active}/><section className="content">{children}</section></main>;
}
