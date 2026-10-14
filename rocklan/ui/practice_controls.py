import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from rocklan.models import SkillType


class PracticeControls(ttk.Frame):
    """White side card for one skill: level, progress bar and a "log practice" input."""

    def __init__(self, parent: tk.Widget, skill: SkillType, on_log: Callable[[int], None]):
        super().__init__(parent, style="Card.TFrame", padding=24)
        self._on_log = on_log

        ttk.Label(self, text="Level", style="CardMuted.TLabel").pack(anchor="w")
        self._level_label = ttk.Label(self, style="CardBig.TLabel")
        self._level_label.pack(anchor="w")
        self._xp_label = ttk.Label(self, style="CardMuted.TLabel")
        self._xp_label.pack(anchor="w", pady=(0, 8))

        self._bar = ttk.Progressbar(self, maximum=100, length=260, style=f"{skill.value}.Horizontal.TProgressbar")
        self._bar.pack(fill="x", pady=(0, 32))

        ttk.Label(self, text="How long did you practice?", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        row = ttk.Frame(self, style="Card.TFrame")
        row.pack(fill="x")
        self._minutes = tk.IntVar(value=30)
        ttk.Spinbox(row, from_=1, to=600, increment=5, width=6, textvariable=self._minutes).pack(side="left")
        ttk.Label(row, text="min", style="Card.TLabel").pack(side="left", padx=6)
        ttk.Button(self, text="Log practice", style="Accent.TButton", cursor="hand2",
                   command=self._log).pack(fill="x", pady=(12, 0))

    def refresh(self, progress: float, level: str, xp: int) -> None:
        self._bar["value"] = progress * 100
        self._level_label["text"] = level
        self._xp_label["text"] = f"{xp} XP  ·  {progress:.0%} polished"

    def _log(self) -> None:
        try:
            minutes = int(self._minutes.get())
        except (tk.TclError, ValueError):
            return  # ignore non-numbers typed into the box
        if minutes > 0:
            self._on_log(minutes)
