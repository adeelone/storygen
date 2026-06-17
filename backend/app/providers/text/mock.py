import asyncio
import re
from collections.abc import AsyncIterator

from app.models import Character, PromptInput, SceneOutline, StoryPlan, WorldBible
from app.providers.base import TextProvider


class MockTextProvider(TextProvider):
    model_name = "storygen-mock-text-v1"

    async def create_plan(self, request: PromptInput) -> StoryPlan:
        core = request.prompt or ", ".join(request.keywords) or request.protagonists[0]
        name = request.protagonists[0] if request.protagonists else "Lumi"
        name = re.sub(r"[^A-Za-z ]", "", name).strip().title() or "Lumi"
        setting = request.setting or "the lantern-lit Mosswhistle Forest"
        friend = "Pip"
        characters = [
            Character(
                name=name,
                species="young squirrel" if "squirrel" in core.lower() else "curious child explorer",
                age="young",
                appearance_tokens=["hazel eyes", "warm chestnut fur", "round cheeks"],
                palette=["chestnut", "moss green", "honey gold"],
                clothing="moss-green satchel and knitted golden scarf",
                accessory="a tiny compass",
                distinguishing_mark="leaf-shaped patch on the satchel",
                personality="brave, kind, and observant",
                signature_pose="one hand on compass, looking upward",
                voice="gentle and determined",
            ),
            Character(
                name=friend,
                species="pocket-sized helper robot",
                age="newly built",
                appearance_tokens=["rounded copper shell", "blue glowing eyes", "two antenna leaves"],
                palette=["copper", "sky blue", "cream"],
                clothing="none",
                accessory="soft blue lantern",
                distinguishing_mark="star stamped on chest",
                personality="loyal, funny, and inventive",
                signature_pose="hovering with lantern held high",
                voice="bright chimes and short cheerful phrases",
            ),
        ]
        ids = [character.id for character in characters]
        style = {
            "watercolor": "soft watercolor children's-book illustration, gentle ink outlines, warm luminous light",
            "gouache": "layered gouache children's-book illustration, velvety color, rounded forms",
            "paper-cut": "handmade paper-cut illustration, textured layers, soft shadows",
        }.get(request.style_preset, "soft watercolor children's-book illustration, gentle outlines")
        return StoryPlan(
            title=f"{name} and the Lantern Trail",
            world=WorldBible(
                setting=setting,
                tone=f"{request.vibe.value}, reassuring, wonder-filled",
                motifs=["floating lanterns", "silver leaves", "little acts of courage"],
                style_descriptor=style,
            ),
            characters=characters,
            scenes=[
                SceneOutline(
                    number=1,
                    arc="Setup",
                    title="A Quiet Glow",
                    location=setting,
                    character_ids=ids,
                    action=f"{name} and {friend} collect glowing seeds for evening lanterns.",
                    emotional_beat="comfortable curiosity",
                ),
                SceneOutline(
                    number=2,
                    arc="Inciting Incident",
                    title="The Lost Light",
                    location="a moonlit creek crossing",
                    character_ids=ids,
                    action="A gust carries the village lantern flame beyond the creek.",
                    emotional_beat="surprise followed by resolve",
                ),
                SceneOutline(
                    number=3,
                    arc="Climax",
                    title="The Brightest Step",
                    location="the whispering hilltop",
                    character_ids=ids,
                    action=f"{name} follows the compass while {friend} lifts the lantern through the wind.",
                    emotional_beat="courage together",
                ),
                SceneOutline(
                    number=4,
                    arc="Resolution",
                    title="Lanterns Home",
                    location="the welcoming village clearing",
                    character_ids=ids,
                    action="They return the flame and share its glow with everyone.",
                    emotional_beat="joy and belonging",
                ),
            ],
        )

    async def stream_scene(self, plan: StoryPlan, scene: SceneOutline, request: PromptInput) -> AsyncIterator[str]:
        lead = plan.characters[0].name
        friend = plan.characters[1].name
        english = {
            1: [
                f"In {plan.world.setting}, {lead} tucked a small compass into a green satchel while {friend}'s lantern hummed a happy tune.",
                "Together they gathered silver leaves, because even a tiny light could make bedtime feel safe and bright.",
            ],
            2: [
                "Just as the first lantern flickered awake, a playful wind swooped down and whisked its golden flame across the creek.",
                f'"We can bring it home," said {lead}. {friend} blinked blue eyes twice: ready, ready.',
            ],
            3: [
                f"The hilltop wind puffed and swirled, but {lead} held the compass steady while {friend} sheltered the wandering flame.",
                "Step by careful step, their two brave lights became one warm beacon that no breeze could scatter.",
            ],
            4: [
                "Back in the clearing, the returned flame skipped from lantern to lantern until the branches looked full of stars.",
                f"{lead} smiled at {friend}. Courage, they learned, glows brightest when friends carry it together.",
            ],
        }
        spanish = {
            1: [
                f"En {plan.world.setting}, {lead} guardó una brújula pequeña mientras la lámpara de {friend} cantaba suave.",
                "Juntos recogieron hojas plateadas para que la noche se sintiera tranquila y luminosa.",
            ],
            2: [
                "Entonces un viento juguetón llevó la llama dorada al otro lado del arroyo.",
                f'"Podemos traerla a casa", dijo {lead}, y {friend} brilló dos veces para decir que sí.',
            ],
            3: [
                f"En la colina, {lead} sostuvo la brújula firme mientras {friend} protegía la llama del viento.",
                "Paso a paso, sus dos luces se unieron en un resplandor que no se apagó.",
            ],
            4: [
                "De vuelta en el claro, la llama saltó de farol en farol hasta llenar las ramas de estrellas.",
                f"{lead} sonrió a {friend}. La valentía brilla más cuando los amigos la comparten.",
            ],
        }
        paragraphs = (spanish if request.language.lower().startswith("spanish") else english)[scene.number]
        if request.length.value == "short":
            paragraphs = paragraphs[:1]
        elif request.length.value == "long":
            paragraphs = paragraphs + [
                f"The memory of {scene.emotional_beat} stayed with them like a warm pocket light."
            ]
        for paragraph in paragraphs:
            await asyncio.sleep(0)
            yield paragraph
