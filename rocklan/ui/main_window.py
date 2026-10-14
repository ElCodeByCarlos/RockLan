import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from rocklan.config import settings
from rocklan.geometry import RockMeshGenerator
from rocklan.models import SkillType
from rocklan.progress import ProgressTracker
from rocklan.ui.home_screen import HomeScreen
from rocklan.ui.skill_screen import SkillScreen
from rocklan.ui.start_screen import StartScreen
from rocklan.ui.theme import apply_theme


class MainWindow:
    """Owns the window and switches between screens:

        Start  ->  Home (4 skill cards)  ->  one Skill page  (Back -> Home)

    It only navigates: the tracker decides progress, each screen draws itself.
    """

    def __init__(self, root: tk.Tk, load_tracker: Callable[[], ProgressTracker], generator: RockMeshGenerator):
        self.root = root
        self.generator = generator
        self._load_tracker = load_tracker
        self.tracker: ProgressTracker | None = None  # loaded when the user presses Start
        self._screen: ttk.Frame | None = None

        root.title(settings.WINDOW_TITLE)
        root.geometry(settings.WINDOW_SIZE)
        root.protocol("WM_DELETE_WINDOW", self._close)
        apply_theme(root)

        self._show(StartScreen(root, on_start=self._start))

    def _show(self, screen: ttk.Frame) -> None:
        if self._screen is not None:
            self._screen.destroy()
        self._screen = screen
        screen.pack(fill="both", expand=True)

    def _start(self) -> None:
        if self.tracker is None:
            self.tracker = self._load_tracker()
        self._open_home()

    def _open_home(self) -> None:
        self._show(HomeScreen(self.root, self.tracker, on_open=self._open_skill))

    def _open_skill(self, skill: SkillType) -> None:
        self._show(SkillScreen(self.root, skill, self.tracker, self.generator, on_back=self._open_home))

    def _close(self) -> None:
        self.root.quit()
        self.root.destroy()
