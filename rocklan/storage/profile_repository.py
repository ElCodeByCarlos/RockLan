import json
from pathlib import Path

from rocklan.models import LearnerProfile


class ProfileRepository:
    """Loads and saves the learner profile as a JSON file.

    To store data somewhere else (SQLite, a server...), write another class
    with the same `load`/`save` methods and pass it to ProgressTracker.
    """

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> LearnerProfile | None:
        if not self.path.exists():
            return None
        with self.path.open(encoding="utf-8") as file:
            return LearnerProfile.from_dict(json.load(file))

    def save(self, profile: LearnerProfile) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Write to a temp file first so a crash can't leave a half-written file.
        temp_path = self.path.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(profile.to_dict(), file, indent=2)
        temp_path.replace(self.path)
