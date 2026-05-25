import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { StoryStream } from "../components/StoryStream";
import { useStoryStore } from "../lib/storyStore";

const draft = {
  id: "1",
  slug: "light",
  status: "draft",
  public: false,
  request: {
    prompt: "glow",
    vibe: "cozy",
    language: "English",
    age_band: "5-7",
  },
  scenes: [],
};
const outline = {
  number: 1,
  arc: "Setup",
  title: "A Glow",
  action: "walk",
  emotional_beat: "wonder",
};
const plan = {
  title: "Lantern Light",
  world: { setting: "forest", tone: "gentle" },
  characters: [],
  scenes: [outline],
};

class FakeSocket {
  static sockets: FakeSocket[] = [];
  onmessage?: (message: MessageEvent<string>) => void;
  onopen?: () => void;
  send = vi.fn();
  close = vi.fn();
  constructor(public url: string) {
    FakeSocket.sockets.push(this);
  }
  message(value: object) {
    this.onmessage?.({ data: JSON.stringify(value) } as MessageEvent<string>);
  }
  open() {
    this.onopen?.();
  }
}

describe("StoryStream", () => {
  beforeEach(() => {
    FakeSocket.sockets = [];
    vi.stubGlobal("WebSocket", FakeSocket);
    vi.stubGlobal("fetch", vi.fn());
    vi.stubGlobal("prompt", vi.fn().mockReturnValue("more fireflies"));
    useStoryStore.setState({
      story: undefined,
      characters: [],
      scenes: {},
      status: "idle",
      error: undefined,
    });
  });

  it("shows its empty state and streams assembled pages", () => {
    const { rerender } = render(<StoryStream />);
    expect(screen.getByText(/illustrated pages/)).toBeInTheDocument();
    useStoryStore.getState().begin(draft);
    rerender(<StoryStream />);
    const socket = FakeSocket.sockets[0];
    act(() => {
      socket.message({ type: "plan_ready", data: { plan } });
      socket.message({
        type: "character_sheet",
        data: {
          character: {
            id: "c",
            name: "Lumi",
            species: "fox",
            clothing: "scarf",
            reference_url: "/c.svg",
          },
        },
      });
      socket.message({
        type: "scene_text",
        data: { scene: 1, paragraph: "A light appeared." },
      });
      socket.message({
        type: "scene_image",
        data: { scene: 1, url: "/one.svg" },
      });
    });
    expect(screen.getByText("Lantern Light")).toBeInTheDocument();
    expect(screen.getByText("A light appeared.")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Cancel"));
    FakeSocket.sockets[1].open();
    expect(FakeSocket.sockets[1].send).toHaveBeenCalled();
  });

  it("requests image and complete-scene regeneration", async () => {
    const complete = {
      ...draft,
      status: "complete",
      plan,
      scenes: [{ outline, paragraphs: ["Done."], image_url: "/one.svg" }],
    };
    useStoryStore
      .getState()
      .accept({ type: "story_complete", data: { story: complete } });
    vi.mocked(fetch).mockResolvedValue({
      json: async () => complete,
    } as Response);
    render(<StoryStream />);
    fireEvent.click(screen.getByText("Adjust picture"));
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByText("Regenerate scene"));
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2));
  });
});
