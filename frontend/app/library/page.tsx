import { LibraryGrid } from "../../components/LibraryGrid";
import { getStories } from "../../lib/api";

export default async function Library() {
  const stories = await getStories();
  return (
    <main className="library">
      <p className="eyebrow">Your shelf</p>
      <h1>My stories</h1>
      <div className="filters">
        <input
          aria-label="Search stories"
          placeholder="Search titles or themes"
        />
        <button className="quiet">All vibes</button>
      </div>
      <LibraryGrid stories={stories} />
    </main>
  );
}
