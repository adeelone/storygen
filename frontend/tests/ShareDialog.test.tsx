import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ShareDialog } from "../components/ShareDialog";

describe("ShareDialog", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true }));
  });
  it("reveals a link after enabling sharing", async () => {
    render(<ShareDialog storyId="1" slug="lantern" />);
    fireEvent.click(screen.getByRole("button", { name: "Create share link" }));
    expect(await screen.findByText(/share\/lantern/)).toBeInTheDocument();
  });
});
