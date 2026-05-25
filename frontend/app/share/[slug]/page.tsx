import { StorybookView } from "../../../components/StorybookView";
import { getSharedStory } from "../../../lib/api";

export default async function SharedStory({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <StorybookView story={await getSharedStory(slug)} />;
}
