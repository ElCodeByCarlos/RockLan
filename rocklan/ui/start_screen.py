import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class StartScreen(ttk.Frame):
    """The first thing the user sees: the app name and a big blue Start button."""

    def __init__(self, parent: tk.Widget, on_start: Callable[[], None]):
        super().__init__(parent)
        center = ttk.Frame(self)
        center.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(center, text="RockLan", style="Title.TLabel").pack()
        ttk.Label(
            center, text="Polish your language skills into perfect spheres", style="Subtitle.TLabel"
        ).pack(pady=(0, 40))

        start = ttk.Button(center, text="Start", style="Start.TButton", command=on_start, cursor="hand2")
        start.pack()
        start.focus_set()  # Enter / Space also starts
        start.bind("<Return>", lambda _event: on_start())
