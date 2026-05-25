import { beforeEach, describe, expect, it } from "vitest";
import { useStoryStore } from "../lib/storyStore";

const story = {
  id: "1",
  slug: "star",
  status: "draft",
  public: false,
  request: {
    prompt: "star",
    vibe: "cozy",
    language: "English",
    age_band: "5-7",
  },
  scenes: [],
};
const outline = {
  number: 1,
  arc: "Setup",
  title: "Home",
  action: "look",
  emotional_beat: "calm",
};

describe("story state", () => {
  beforeEach(() =>
    useStoryStore.setState({
      story: undefined,
      characters: [],
      scenes: {},
      status: "idle",
      error: undefined,
    }),
  );

  it("assembles streamed story state", () => {
    useStoryStore.getState().begin(story);
    useStoryStore.getState().accept({
      type: "plan_ready",
      data: {
        plan: {
          title: "Star",
          world: { setting: "sky", tone: "soft" },
          characters: [],
          scenes: [outline],
        },
      },
    });
    useStoryStore
      .getState()
      .accept({ type: "scene_text", data: { scene: 1, paragraph: "Hello." } });
    useStoryStore
      .getState()
      .accept({ type: "scene_image", data: { scene: 1, url: "/one.svg" } });
    expect(useStoryStore.getState().scenes[1].paragraphs).toEqual(["Hello."]);
    expect(useStoryStore.getState().scenes[1].image_url).toBe("/one.svg");
  });

  it("records characters, errors, and completion replacements", () => {
    useStoryStore.getState().begin(story);
    useStoryStore.getState().accept({
      type: "character_sheet",
      data: {
        character: {
          id: "c",
          name: "Lumi",
          species: "fox",
          clothing: "scarf",
        },
      },
    });
    useStoryStore
      .getState()
      .accept({ type: "error", data: { message: "gentler idea" } });
    expect(useStoryStore.getState().characters).toHaveLength(1);
    expect(useStoryStore.getState().error).toBe("gentler idea");
    useStoryStore.getState().accept({
      type: "story_complete",
      data: {
        story: {
          ...story,
          status: "complete",
          scenes: [{ outline, paragraphs: ["Done."] }],
        },
      },
    });
    expect(useStoryStore.getState().status).toBe("complete");
  });
});
