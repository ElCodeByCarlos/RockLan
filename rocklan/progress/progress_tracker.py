from rocklan.config import settings
from rocklan.models import LearnerProfile, SkillProgress, SkillType
from rocklan.progress.level_calculator import LevelCalculator
from rocklan.storage import ProfileRepository


class ProgressTracker:
    """The one place where progress changes.

    The UI calls this instead of editing the profile directly, so the rules
    (how much XP a minute is worth, saving after each change) live here.
    """

    def __init__(
        self,
        profile: LearnerProfile,
        calculator: LevelCalculator,
        repository: ProfileRepository | None = None,
    ):
        self.profile = profile
        self.calculator = calculator
        self.repository = repository  # None = don't save (demo mode)

    def log_practice(self, skill: SkillType, minutes: int) -> SkillProgress:
        progress = self.profile.get(skill)
        gained = max(0, minutes) * settings.XP_PER_MINUTE
        progress.xp = min(progress.xp + gained, self.calculator.max_xp)
        self._save()
        return progress

    def set_language(self, language: str) -> None:
        self.profile.target_language = language
        self._save()

    def progress_of(self, skill: SkillType) -> float:
        return self.calculator.progress(self.profile.get(skill).xp)

    def level_of(self, skill: SkillType) -> str:
        return self.calculator.level(self.profile.get(skill).xp)

    def _save(self) -> None:
        if self.repository is not None:
            self.repository.save(self.profile)
