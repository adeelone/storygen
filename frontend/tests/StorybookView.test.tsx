import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { StorybookView } from "../components/StorybookView";

describe("StorybookView", () => {
  it("provides a narration action", () => {
    const speak = vi.fn();
    vi.stubGlobal("speechSynthesis", { speak });
    vi.stubGlobal("SpeechSynthesisUtterance", function (text: string) {
      return { text };
    });
    render(
      <StorybookView
        story={{
          id: "1",
          slug: "lights",
          status: "complete",
          public: false,
          request: {
            prompt: "",
            vibe: "cozy",
            language: "English",
            age_band: "5-7",
          },
          scenes: [],
        }}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: "Narrate aloud" }));
    expect(speak).toHaveBeenCalled();
  });
});
