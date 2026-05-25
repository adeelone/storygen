import Link from "next/link";
import Image from "next/image";
import { mediaUrl } from "../lib/api";
import { Story } from "../lib/types";

export function LibraryGrid({ stories }: { stories: Story[] }) {
  return (
    <div className="library-grid">
      {stories.map((story) => (
        <Link className="cover" href={`/story/${story.id}`} key={story.id}>
          {story.scenes[0]?.image_url ? (
            <Image
              src={mediaUrl(story.scenes[0].image_url)!}
              width={720}
              height={960}
              unoptimized
              alt=""
            />
          ) : (
            <div className="cover-blank" />
          )}
          <h2>{story.plan?.title ?? story.slug}</h2>
          <p>
            {story.request.vibe} - {story.request.age_band}
          </p>
        </Link>
      ))}
      {!stories.length ? (
        <p>No stories yet. Begin one on the home page.</p>
      ) : null}
    </div>
  );
}
