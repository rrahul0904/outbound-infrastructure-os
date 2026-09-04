import type { LucideIcon } from "lucide-react";

export function MetricCard({ label, value, helper, icon: Icon, tone = "default" }: { label: string; value: string; helper: string; icon: LucideIcon; tone?: "default" | "good" | "warn"; }) {
  return <article className={`metricCard ${tone}`}><div className="metricTop"><span>{label}</span><div className="iconTile"><Icon size={17}/></div></div><strong>{value}</strong><small>{helper}</small></article>;
}
