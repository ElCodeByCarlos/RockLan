import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from rocklan.config import settings
from rocklan.geometry import RockMeshGenerator
from rocklan.models import SkillType
from rocklan.progress import ProgressTracker
from rocklan.ui.practice_controls import PracticeControls
from rocklan.ui.rock_view import RockView


class SkillScreen(ttk.Frame):
    """The page for one skill: its rock on the left, level + "log practice" on the right."""

    def __init__(self, parent: tk.Widget, skill: SkillType, tracker: ProgressTracker,
                 generator: RockMeshGenerator, on_back: Callable[[], None]):
        super().__init__(parent)
        self.skill = skill
        self.tracker = tracker

        top = ttk.Frame(self, padding=(24, 16, 24, 0))
        top.pack(fill="x")
        ttk.Button(top, text="←  All skills", style="Link.TButton", cursor="hand2",
                   command=on_back).pack(side="left")
        ttk.Label(top, text=skill.label, style="Heading.TLabel").pack(side="left", padx=16)

        self.controls = PracticeControls(self, skill, on_log=self._log_practice)
        self.controls.pack(side="right", fill="y", padx=24, pady=24)

        rock_frame = tk.Frame(self, background=settings.BACKGROUND_COLOR)
        rock_frame.pack(side="left", fill="both", expand=True)
        self.rock = RockView(rock_frame, generator)

        self._refresh()

    def _log_practice(self, minutes: int) -> None:
        self.tracker.log_practice(self.skill, minutes)
        self._refresh()

    def _refresh(self) -> None:
        progress = self.tracker.progress_of(self.skill)
        data = self.tracker.profile.get(self.skill)
        self.rock.show(self.skill, progress, data.rock_seed)
        self.controls.refresh(progress, self.tracker.level_of(self.skill), data.xp)
