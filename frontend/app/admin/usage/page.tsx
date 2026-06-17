import Link from "next/link";
import { getUsage } from "../../../lib/api";

export default async function UsagePage({
  searchParams,
}: {
  searchParams: Promise<{ key?: string }>;
}) {
  const { key } = await searchParams;
  const usage = await getUsage(key);
  return (
    <main className="admin">
      <p className="eyebrow">Admin</p>
      <h1>Usage</h1>
      <div className="metric-grid">
        <article>
          <span>Stories today</span>
          <strong>{usage.stories_today}</strong>
        </article>
        <article>
          <span>Images today</span>
          <strong>{usage.images_today}</strong>
        </article>
        <article>
          <span>Estimated cost</span>
          <strong>${usage.estimated_cost_usd_today.toFixed(4)}</strong>
        </article>
      </div>
      <Link
        className="quiet"
        href={`/admin/eval${key ? `?key=${encodeURIComponent(key)}` : ""}`}
      >
        View evaluation report
      </Link>
    </main>
  );
}
