import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SceneCard } from "../components/SceneCard";

describe("SceneCard", () => {
  it("shows streamed prose and illustration", () => {
    const adjust = vi.fn();
    const regenerate = vi.fn();
    render(
      <SceneCard
        scene={{
          outline: {
            number: 1,
            arc: "Setup",
            title: "Dawn",
            action: "walk",
            emotional_beat: "wonder",
          },
          paragraphs: ["Hello forest."],
          image_url: "/assets/picture.svg",
        }}
        onReroll={adjust}
        onRegenerate={regenerate}
      />,
    );
    expect(screen.getByText("Hello forest.")).toBeInTheDocument();
    expect(screen.getByAltText("Illustration for Dawn")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Adjust picture"));
    fireEvent.click(screen.getByText("Regenerate scene"));
    expect(adjust).toHaveBeenCalledWith(1);
    expect(regenerate).toHaveBeenCalledWith(1);
  });
});
