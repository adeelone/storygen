"use client";

import { useState } from "react";

export function ShareDialog({
  storyId,
  slug,
}: {
  storyId: string;
  slug: string;
}) {
  const [shared, setShared] = useState(false);
  async function enableShare() {
    await fetch(
      `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/stories/${storyId}/share`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ expires_days: 30 }),
      },
    );
    setShared(true);
  }
  return (
    <aside className="share">
      <button className="quiet" onClick={enableShare}>
        {shared ? "Link ready" : "Create share link"}
      </button>
      {shared ? <code>{`${window.location.origin}/share/${slug}`}</code> : null}
    </aside>
  );
}
