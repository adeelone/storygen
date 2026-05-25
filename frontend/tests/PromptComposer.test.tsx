import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { PromptComposer } from "../components/PromptComposer";
import { useStoryStore } from "../lib/storyStore";

describe("PromptComposer", () => {
  beforeEach(() => {
    useStoryStore.setState({
      story: undefined,
      characters: [],
      scenes: {},
      status: "idle",
      error: undefined,
    });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          id: "1",
          slug: "new",
          status: "draft",
          request: {},
          scenes: [],
        }),
      }),
    );
  });

  it("offers free text and keyword creation modes", () => {
    render(<PromptComposer />);
    const submit = screen.getByRole("button", { name: "Create my story" });
    expect(submit).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "ocean" }));
    expect(submit).toBeEnabled();
  });

  it("creates a guided story request", async () => {
    render(<PromptComposer />);
    fireEvent.click(screen.getByText("Use guided bedtime settings"));
    fireEvent.click(screen.getByRole("button", { name: "Create my story" }));
    await waitFor(() =>
      expect(useStoryStore.getState().status).toBe("creating"),
    );
    expect(fetch).toHaveBeenCalled();
  });
});
