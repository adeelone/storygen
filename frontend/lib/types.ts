export type Character = {
  id: string;
  name: string;
  species: string;
  reference_url?: string;
  clothing: string;
};
export type Outline = {
  number: number;
  arc: string;
  title: string;
  action: string;
  emotional_beat: string;
};
export type Plan = {
  title: string;
  characters: Character[];
  scenes: Outline[];
  world: { setting: string; tone: string };
};
export type Scene = {
  outline: Outline;
  paragraphs: string[];
  image_url?: string;
};
export type Story = {
  id: string;
  slug: string;
  status: string;
  public: boolean;
  request: {
    prompt: string;
    vibe: string;
    language: string;
    age_band: string;
    length?: string;
    aspect_ratio?: string;
    style_preset?: string;
  };
  plan?: Plan;
  scenes: Scene[];
};
export type UsageSummary = {
  stories_today: number;
  images_today: number;
  estimated_cost_usd_today: number;
};
export type EvalSummary = {
  score: number;
  threshold: number;
  passed: boolean;
  cases: { prompt: string; score: number; checks: Record<string, boolean> }[];
};
export type StreamEvent =
  | { type: "plan_ready"; data: { plan: Plan } }
  | { type: "character_sheet"; data: { character: Character } }
  | { type: "scene_text"; data: { scene: number; paragraph: string } }
  | { type: "scene_image"; data: { scene: number; url: string } }
  | { type: "scene_complete"; data: { scene: number } }
  | { type: "story_complete"; data: { story: Story } }
  | { type: "error"; data: { message: string; suggested_rewrite?: string } };
