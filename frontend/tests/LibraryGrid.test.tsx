import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LibraryGrid } from "../components/LibraryGrid";

describe("LibraryGrid", () => {
  it("renders completed covers and the empty shelf", () => {
    const { rerender } = render(
      <LibraryGrid
        stories={[
          {
            id: "1",
            slug: "light",
            status: "complete",
            public: false,
            request: {
              prompt: "",
              vibe: "cozy",
              language: "English",
              age_band: "5-7",
            },
            plan: {
              title: "Lanterns",
              world: { setting: "", tone: "" },
              characters: [],
              scenes: [],
            },
            scenes: [
              {
                outline: {
                  number: 1,
                  arc: "Setup",
                  title: "Glow",
                  action: "",
                  emotional_beat: "",
                },
                paragraphs: [],
                image_url: "/one.svg",
              },
            ],
          },
        ]}
      />,
    );
    expect(screen.getByText("Lanterns")).toBeInTheDocument();
    rerender(<LibraryGrid stories={[]} />);
    expect(screen.getByText(/No stories yet/)).toBeInTheDocument();
  });
});
