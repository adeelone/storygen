import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  createStory,
  getSharedStory,
  getStories,
  getStory,
  getEval,
  getUsage,
  mediaUrl,
  narrationUrl,
  websocketUrl,
} from "../lib/api";

describe("API client", () => {
  beforeEach(() => vi.stubGlobal("fetch", vi.fn()));

  it("loads stories and shared stories", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => [{ id: "1" }],
    } as Response);
    expect(
      await getStories({ q: "star", vibe: "cozy", language: "English" }),
    ).toHaveLength(1);
    expect(vi.mocked(fetch).mock.calls[0][0]).toContain("q=star");
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({ id: "1" }),
    } as Response);
    expect((await getStory("1")).id).toBe("1");
    expect((await getSharedStory("shared")).id).toBe("1");
  });

  it("posts new story requests and builds media protocols", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ id: "new" }),
    } as Response);
    expect((await createStory({ prompt: "star" })).id).toBe("new");
    expect(mediaUrl("/assets/one.svg")).toContain(
      "http://localhost:8000/assets",
    );
    expect(mediaUrl("https://cdn/image")).toBe("https://cdn/image");
    expect(websocketUrl("session")).toBe("ws://localhost:8000/ws/session");
    expect(narrationUrl("new")).toContain("/stories/new/narration");
  });

  it("loads admin summaries", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        stories_today: 1,
        images_today: 2,
        estimated_cost_usd_today: 0.04,
      }),
    } as Response);
    expect((await getUsage("key")).stories_today).toBe(1);
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ score: 1, threshold: 0.8, passed: true, cases: [] }),
    } as Response);
    expect((await getEval("key")).passed).toBe(true);
  });

  it("handles not-found responses", async () => {
    vi.mocked(fetch).mockResolvedValue({ ok: false } as Response);
    await expect(getStory("missing")).rejects.toThrow();
    await expect(getSharedStory("missing")).rejects.toThrow();
    await expect(createStory({ prompt: "none" })).rejects.toThrow();
    await expect(getUsage()).rejects.toThrow();
    await expect(getEval()).rejects.toThrow();
    expect(await getStories()).toEqual([]);
  });
});
