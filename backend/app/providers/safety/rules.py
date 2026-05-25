import re

from app.providers.base import SafetyProvider


class RulesSafetyProvider(SafetyProvider):
    _always_block = (r"\bslur\b", r"\bgraphic gore\b", r"\bkill (?:a|the) real\b")
    _young_block = (r"\bweapon\b", r"\bblood\b", r"\bterror\b")

    async def screen(self, text: str, age_band: str) -> tuple[bool, str | None]:
        patterns = self._always_block + (self._young_block if age_band == "3-5" else ())
        if any(re.search(pattern, text.lower()) for pattern in patterns):
            return False, "Try a gentle adventure with a surprising problem and a kind solution."
        return True, None
