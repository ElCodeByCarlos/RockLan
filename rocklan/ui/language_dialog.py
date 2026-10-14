import tkinter as tk
from tkinter import ttk

from rocklan.config import settings
from rocklan.ui.theme import FONT


def ask_language(parent: tk.Misc, title: str, initial: str | None = None) -> str | None:
    """Show a scrollable list of languages. Returns the choice, or None if cancelled."""
    return LanguageDialog(parent, title, initial).result


class LanguageDialog(tk.Toplevel):
    """Modal window with a scrollable language list plus OK / Cancel."""

    def __init__(self, parent: tk.Misc, title: str, initial: str | None):
        super().__init__(parent, background=settings.BACKGROUND_COLOR, padx=24, pady=20)
        self.result: str | None = None
        self.title(title)
        self.resizable(False, False)
        self.transient(parent.winfo_toplevel())

        languages = list(settings.LANGUAGES)
        if initial and initial not in languages:
            languages.insert(0, initial)  # keep a language saved before this list existed

        ttk.Label(self, text="Which language do you want to learn?", style="TLabel",
                  font=(FONT, 13, "bold")).pack(anchor="w", pady=(0, 10))

        box = ttk.Frame(self)
        box.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(box, orient="vertical")
        self._list = tk.Listbox(
            box, height=10, width=28, font=(FONT, 12), activestyle="none", exportselection=False,
            background=settings.PANEL_COLOR, foreground=settings.TEXT_COLOR,
            selectbackground=settings.ACCENT_COLOR, selectforeground=settings.ACCENT_TEXT_COLOR,
            highlightthickness=1, highlightbackground=settings.BORDER_COLOR,
            highlightcolor=settings.ACCENT_COLOR, borderwidth=6, relief="flat",  # border = inner padding
            yscrollcommand=scrollbar.set,
        )
        scrollbar.configure(command=self._list.yview)
        self._list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for language in languages:
            self._list.insert("end", language)

        index = languages.index(initial) if initial in languages else 0
        self._list.selection_set(index)
        self._list.activate(index)
        self._list.see(index)
        self._list.focus_set()

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", pady=(16, 0))
        ttk.Button(buttons, text="OK", style="Accent.TButton", cursor="hand2",
                   command=self._ok).pack(side="right")
        ttk.Button(buttons, text="Cancel", style="Link.TButton", cursor="hand2",
                   command=self.destroy).pack(side="right", padx=12)

        self._list.bind("<Double-Button-1>", lambda _event: self._ok())
        self.bind("<Return>", lambda _event: self._ok())
        self.bind("<Escape>", lambda _event: self.destroy())

        self._center_on(parent.winfo_toplevel())
        self.grab_set()
        self.wait_window()

    def _ok(self) -> None:
        selection = self._list.curselection()
        if selection:
            self.result = self._list.get(selection[0])
        self.destroy()

    def _center_on(self, window: tk.Misc) -> None:
        self.update_idletasks()
        x = window.winfo_rootx() + (window.winfo_width() - self.winfo_reqwidth()) // 2
        y = window.winfo_rooty() + (window.winfo_height() - self.winfo_reqheight()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
