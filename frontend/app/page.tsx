import { PromptComposer } from "../components/PromptComposer";
import { StoryStream } from "../components/StoryStream";

export default function Home() {
  return (
    <main className="home">
      <section className="hero">
        <p className="eyebrow">Illustrated stories in moments</p>
        <h1>Where little ideas become luminous adventures.</h1>
        <p className="intro">
          Choose a few words. StoryGen writes and paints four gentle chapters
          while you watch.
        </p>
        <PromptComposer />
      </section>
      <StoryStream />
    </main>
  );
}
