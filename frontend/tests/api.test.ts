import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  createStory,
  getSharedStory,
  getStories,
  getStory,
  mediaUrl,
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
    expect(await getStories()).toHaveLength(1);
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
  });

  it("handles not-found responses", async () => {
    vi.mocked(fetch).mockResolvedValue({ ok: false } as Response);
    await expect(getStory("missing")).rejects.toThrow();
    await expect(getSharedStory("missing")).rejects.toThrow();
    await expect(createStory({ prompt: "none" })).rejects.toThrow();
    expect(await getStories()).toEqual([]);
  });
});
