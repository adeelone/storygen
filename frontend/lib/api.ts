import { EvalSummary, Story, UsageSummary } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function createStory(
  body: Record<string, unknown>,
): Promise<Story> {
  const response = await fetch(`${API}/api/v1/stories`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error("Could not begin this story.");
  return response.json() as Promise<Story>;
}

export async function getStories(
  filters: { q?: string; vibe?: string; language?: string } = {},
): Promise<Story[]> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  const suffix = params.size ? `?${params.toString()}` : "";
  const response = await fetch(`${API}/api/v1/stories${suffix}`, {
    cache: "no-store",
  });
  return response.ok ? (response.json() as Promise<Story[]>) : [];
}

export async function getStory(id: string): Promise<Story> {
  const response = await fetch(`${API}/api/v1/stories/${id}`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Story not found");
  return response.json() as Promise<Story>;
}

export async function getSharedStory(slug: string): Promise<Story> {
  const response = await fetch(`${API}/api/v1/shares/${slug}`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error("Shared story not found");
  return response.json() as Promise<Story>;
}

export function mediaUrl(url?: string): string | undefined {
  return url?.startsWith("/") ? `${API}${url}` : url;
}

export function websocketUrl(sessionId: string): string {
  return `${API.replace("http", "ws")}/ws/${sessionId}`;
}

export function narrationUrl(storyId: string): string {
  return `${API}/api/v1/stories/${storyId}/narration`;
}

export async function getUsage(adminKey?: string): Promise<UsageSummary> {
  const response = await fetch(`${API}/api/v1/admin/usage`, {
    cache: "no-store",
    headers: adminKey ? { "x-admin-key": adminKey } : {},
  });
  if (!response.ok) throw new Error("Usage dashboard is locked.");
  return response.json() as Promise<UsageSummary>;
}

export async function getEval(adminKey?: string): Promise<EvalSummary> {
  const response = await fetch(`${API}/api/v1/admin/eval`, {
    cache: "no-store",
    headers: adminKey ? { "x-admin-key": adminKey } : {},
  });
  if (!response.ok) throw new Error("Evaluation dashboard is locked.");
  return response.json() as Promise<EvalSummary>;
}
