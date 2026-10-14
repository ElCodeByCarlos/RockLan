import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from rocklan.config import settings
from rocklan.models import SkillType
from rocklan.progress import ProgressTracker
from rocklan.ui.language_dialog import ask_language
from rocklan.ui.theme import FONT


class SkillCard(tk.Frame):
    """A clickable card for one skill. Clicking anywhere on it opens that skill's page."""

    def __init__(self, parent: tk.Widget, skill: SkillType, tracker: ProgressTracker,
                 on_open: Callable[[SkillType], None]):
        super().__init__(
            parent, background=settings.PANEL_COLOR, cursor="hand2",
            highlightthickness=2, highlightbackground=settings.BORDER_COLOR,
        )
        self._on_click = lambda _event: on_open(skill)
        panel, color = settings.PANEL_COLOR, settings.SKILL_COLORS[skill.value]
        progress, level, xp = tracker.progress_of(skill), tracker.level_of(skill), tracker.profile.get(skill).xp

        tk.Frame(self, background=color, height=8).pack(fill="x")
        body = tk.Frame(self, background=panel, padx=24, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=skill.label, background=panel, foreground=settings.TEXT_COLOR,
                 font=(FONT, 20, "bold")).pack(anchor="w")
        tk.Label(body, text=f"Level {level}  ·  {xp} XP", background=panel,
                 foreground=settings.MUTED_TEXT_COLOR, font=(FONT, 11)).pack(anchor="w", pady=(2, 12))
        ttk.Progressbar(body, maximum=100, value=progress * 100,
                        style=f"{skill.value}.Horizontal.TProgressbar").pack(fill="x")
        tk.Label(body, text=f"{progress:.0%} polished", background=panel,
                 foreground=settings.MUTED_TEXT_COLOR, font=(FONT, 10)).pack(anchor="w", pady=(4, 0))
        tk.Label(body, text="Practice  →", background=panel, foreground=settings.ACCENT_COLOR,
                 font=(FONT, 12, "bold")).pack(anchor="e", side="bottom")

        for widget in self._all_widgets(self):
            widget.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda _event: self._set_hover(True))
        self.bind("<Leave>", self._on_leave)

    def _all_widgets(self, widget: tk.Misc) -> list[tk.Misc]:
        result = [widget]
        for child in widget.winfo_children():
            result.extend(self._all_widgets(child))
        return result

    def _on_leave(self, event: tk.Event) -> None:
        # Moving onto a child label also fires <Leave>; only un-hover if the pointer left the card.
        under_pointer = self.winfo_containing(event.x_root, event.y_root)
        if under_pointer is None or not str(under_pointer).startswith(str(self)):
            self._set_hover(False)

    def _set_hover(self, hovered: bool) -> None:
        self["highlightbackground"] = settings.ACCENT_COLOR if hovered else settings.BORDER_COLOR


class HomeScreen(ttk.Frame):
    """The four skill categories. Each card opens its own practice page."""

    def __init__(self, parent: tk.Widget, tracker: ProgressTracker, on_open: Callable[[SkillType], None]):
        super().__init__(parent, padding=32)
        self.tracker = tracker

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 24))
        ttk.Label(header, text="Choose a skill to practice", style="Heading.TLabel").pack(side="left")
        ttk.Button(header, text="Change", style="Link.TButton", cursor="hand2",
                   command=self._change_language).pack(side="right")
        self._language_label = ttk.Label(header, style="Subtitle.TLabel")
        self._language_label.pack(side="right", padx=8)
        self._update_language_label()

        grid = ttk.Frame(self)
        grid.pack(fill="both", expand=True)
        for index, skill in enumerate(SkillType):
            row, column = divmod(index, 2)
            SkillCard(grid, skill, tracker, on_open).grid(row=row, column=column, sticky="nsew", padx=12, pady=12)
        grid.columnconfigure((0, 1), weight=1, uniform="card")
        grid.rowconfigure(tuple(range((len(SkillType) + 1) // 2)), weight=1, uniform="card")

    def _update_language_label(self) -> None:
        self._language_label["text"] = f"Learning: {self.tracker.profile.target_language}"

    def _change_language(self) -> None:
        language = ask_language(self, "Language", initial=self.tracker.profile.target_language)
        if language:
            self.tracker.set_language(language)
            self._update_language_label()
