import { getEval } from "../../../lib/api";

export default async function EvalPage({
  searchParams,
}: {
  searchParams: Promise<{ key?: string }>;
}) {
  const { key } = await searchParams;
  const report = await getEval(key);
  return (
    <main className="admin">
      <p className="eyebrow">Admin</p>
      <h1>Evaluation</h1>
      <div className="metric-grid">
        <article>
          <span>Score</span>
          <strong>{report.score.toFixed(2)}</strong>
        </article>
        <article>
          <span>Threshold</span>
          <strong>{report.threshold.toFixed(2)}</strong>
        </article>
        <article>
          <span>Status</span>
          <strong>{report.passed ? "Pass" : "Fail"}</strong>
        </article>
      </div>
      <div className="eval-table">
        {report.cases.map((item) => (
          <article key={item.prompt}>
            <h2>{item.prompt}</h2>
            <p>Score: {item.score.toFixed(2)}</p>
          </article>
        ))}
      </div>
    </main>
  );
}
