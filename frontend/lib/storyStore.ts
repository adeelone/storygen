import { create } from "zustand";
import { Character, Plan, Scene, Story, StreamEvent } from "./types";

type State = {
  story?: Story;
  characters: Character[];
  scenes: Record<number, Scene>;
  status: string;
  error?: string;
  begin: (story: Story) => void;
  accept: (event: StreamEvent) => void;
};

export const useStoryStore = create<State>((set) => ({
  characters: [],
  scenes: {},
  status: "idle",
  begin: (story) =>
    set({
      story,
      characters: [],
      scenes: {},
      status: "creating",
      error: undefined,
    }),
  accept: (event) =>
    set((state) => {
      if (event.type === "plan_ready") {
        const scenes = Object.fromEntries(
          event.data.plan.scenes.map((outline) => [
            outline.number,
            { outline, paragraphs: [] },
          ]),
        );
        return {
          story: { ...state.story!, plan: event.data.plan },
          scenes,
          status: "illustrating",
        };
      }
      if (event.type === "character_sheet")
        return { characters: [...state.characters, event.data.character] };
      if (event.type === "scene_text") {
        const scene = state.scenes[event.data.scene];
        return {
          scenes: {
            ...state.scenes,
            [event.data.scene]: {
              ...scene,
              paragraphs: [...scene.paragraphs, event.data.paragraph],
            },
          },
          status: "writing",
        };
      }
      if (event.type === "scene_image") {
        const scene = state.scenes[event.data.scene];
        return {
          scenes: {
            ...state.scenes,
            [event.data.scene]: { ...scene, image_url: event.data.url },
          },
        };
      }
      if (event.type === "story_complete") {
        return {
          story: event.data.story,
          scenes: Object.fromEntries(
            event.data.story.scenes.map((scene) => [
              scene.outline.number,
              scene,
            ]),
          ),
          status: "complete",
        };
      }
      if (event.type === "error")
        return { status: "error", error: event.data.message };
      return {};
    }),
}));
