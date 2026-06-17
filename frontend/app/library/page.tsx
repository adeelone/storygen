import { LibraryGrid } from "../../components/LibraryGrid";
import { getStories } from "../../lib/api";

export default async function Library({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; vibe?: string; language?: string }>;
}) {
  const filters = await searchParams;
  const stories = await getStories(filters);
  return (
    <main className="library">
      <p className="eyebrow">Your shelf</p>
      <h1>My stories</h1>
      <form className="filters">
        <input
          aria-label="Search stories"
          name="q"
          defaultValue={filters.q ?? ""}
          placeholder="Search titles or themes"
        />
        <select
          className="quiet"
          name="vibe"
          defaultValue={filters.vibe ?? ""}
          aria-label="Filter by vibe"
        >
          <option value="">All vibes</option>
          <option value="cozy">Cozy</option>
          <option value="adventurous">Adventurous</option>
          <option value="silly">Silly</option>
          <option value="bedtime">Bedtime</option>
        </select>
        <select
          className="quiet"
          name="language"
          defaultValue={filters.language ?? ""}
          aria-label="Filter by language"
        >
          <option value="">All languages</option>
          <option value="English">English</option>
          <option value="Spanish">Spanish</option>
        </select>
        <button className="primary compact">Filter</button>
      </form>
      <LibraryGrid stories={stories} />
    </main>
  );
}
