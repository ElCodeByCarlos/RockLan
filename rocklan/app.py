import tkinter as tk

from rocklan.config import settings
from rocklan.geometry import RockMeshGenerator
from rocklan.models import LearnerProfile, SkillType
from rocklan.progress import LevelCalculator, ProgressTracker
from rocklan.storage import ProfileRepository
from rocklan.ui import MainWindow
from rocklan.ui.language_dialog import ask_language

DEFAULT_LANGUAGE = "Spanish"


def run(demo: bool = False) -> None:
    """Create every piece of the app, connect them, and start the window."""
    root = tk.Tk()
    calculator = LevelCalculator()
    # The profile is loaded after the user presses Start, so the Start screen is always first.
    MainWindow(root, lambda: _load_tracker(root, calculator, demo), RockMeshGenerator())
    root.mainloop()


def _load_tracker(root: tk.Tk, calculator: LevelCalculator, demo: bool) -> ProgressTracker:
    if demo:
        return ProgressTracker(_demo_profile(calculator), calculator, repository=None)

    repository = ProfileRepository(settings.PROFILE_FILE)
    profile = repository.load()
    if profile is None:
        language = ask_language(root, "Welcome to RockLan", initial=DEFAULT_LANGUAGE)
        profile = LearnerProfile.new(language or DEFAULT_LANGUAGE)
        repository.save(profile)
    return ProgressTracker(profile, calculator, repository)


def _demo_profile(calculator: LevelCalculator) -> LearnerProfile:
    """Four rocks at 0%, 33%, 66% and 100% so you can see the whole journey."""
    profile = LearnerProfile.new("Demo")
    for index, skill in enumerate(SkillType):
        profile.get(skill).xp = round(calculator.max_xp * index / 3)
    return profile
