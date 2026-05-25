import { Story } from "./types";

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

export async function getStories(): Promise<Story[]> {
  const response = await fetch(`${API}/api/v1/stories`, { cache: "no-store" });
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
