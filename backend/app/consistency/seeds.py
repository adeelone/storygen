import hashlib


def stable_seed(story_id: str, character_id: str) -> int:
    digest = hashlib.sha256(f"{story_id}:{character_id}".encode()).hexdigest()
    return int(digest[:8], 16) % 2_147_483_647
