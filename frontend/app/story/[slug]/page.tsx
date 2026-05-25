import { ShareDialog } from "../../../components/ShareDialog";
import { StorybookView } from "../../../components/StorybookView";
import { getStory } from "../../../lib/api";

export default async function ReadStory({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const story = await getStory(slug);
  return (
    <>
      <ShareDialog storyId={story.id} slug={story.slug} />
      <StorybookView story={story} />
    </>
  );
}
