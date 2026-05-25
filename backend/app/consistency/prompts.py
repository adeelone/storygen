from app.models import Character, SceneOutline, StoryPlan


def token_block(characters: list[Character]) -> str:
    blocks = []
    for character in sorted(characters, key=lambda item: item.id):
        tokens = ", ".join(character.appearance_tokens)
        palette = ", ".join(character.palette)
        blocks.append(
            f"[{character.name}] species={character.species}; appearance={tokens}; "
            f"palette={palette}; clothing={character.clothing}; accessory={character.accessory}; "
            f"mark={character.distinguishing_mark}"
        )
    return "\n".join(blocks)


def build_reference_prompt(character: Character, style_descriptor: str) -> str:
    return (
        f"CHARACTER REFERENCE SHEET. {style_descriptor}. Front view, three-quarter view, and happy expression. "
        f"Keep identical details in every view.\n{token_block([character])}"
    )


def build_scene_prompt(plan: StoryPlan, scene: SceneOutline) -> str:
    present = [character for character in plan.characters if character.id in scene.character_ids]
    return (
        "STYLE LOCK:\n"
        f"{plan.world.style_descriptor}.\n"
        "CHARACTER TOKEN LOCK - do not alter these identifiers:\n"
        f"{token_block(present)}\n"
        "COMPOSITION:\n"
        f"{scene.location}; {scene.action}; emotional beat: {scene.emotional_beat}. "
        "Expressive, child-safe picture book composition with no text."
    )
