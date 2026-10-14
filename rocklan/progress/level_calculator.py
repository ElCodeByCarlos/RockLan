from rocklan.config import settings

# (level name, progress fraction needed to reach it), lowest first.
CEFR_LEVELS = [
    ("A1", 0.0),
    ("A2", 1 / 6),
    ("B1", 2 / 6),
    ("B2", 3 / 6),
    ("C1", 4 / 6),
    ("C2", 5 / 6),
    ("Mastery", 1.0),
]


class LevelCalculator:
    """Turns raw XP into a 0..1 progress value and a CEFR level name."""

    def __init__(self, max_xp: int = settings.MAX_XP):
        self.max_xp = max_xp

    def progress(self, xp: int) -> float:
        return max(0.0, min(xp / self.max_xp, 1.0))

    def level(self, xp: int) -> str:
        progress = self.progress(xp)
        current = CEFR_LEVELS[0][0]
        for name, threshold in CEFR_LEVELS:
            if progress >= threshold:
                current = name
        return current
