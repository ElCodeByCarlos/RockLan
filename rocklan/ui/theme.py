import tkinter as tk
from tkinter import ttk

from rocklan.config import settings

FONT = "Segoe UI"


def apply_theme(root: tk.Tk) -> None:
    """Light-blue ttk styles shared by every screen."""
    root.configure(background=settings.BACKGROUND_COLOR)
    style = ttk.Style(root)
    style.theme_use("clam")

    bg, panel, text = settings.BACKGROUND_COLOR, settings.PANEL_COLOR, settings.TEXT_COLOR
    muted = settings.MUTED_TEXT_COLOR

    # Plain frames/labels sit on the page background; "Card" ones on white.
    style.configure("TFrame", background=bg)
    style.configure("Card.TFrame", background=panel)
    style.configure("TLabel", background=bg, foreground=text, font=(FONT, 11))
    style.configure("Title.TLabel", background=bg, foreground=settings.ACCENT_COLOR, font=(FONT, 48, "bold"))
    style.configure("Subtitle.TLabel", background=bg, foreground=muted, font=(FONT, 14))
    style.configure("Heading.TLabel", background=bg, foreground=text, font=(FONT, 22, "bold"))
    style.configure("Card.TLabel", background=panel, foreground=text, font=(FONT, 11))
    style.configure("CardMuted.TLabel", background=panel, foreground=muted, font=(FONT, 11))
    style.configure("CardBig.TLabel", background=panel, foreground=text, font=(FONT, 28, "bold"))

    _blue_button(style, "Accent.TButton", font=(FONT, 11, "bold"), padding=(16, 8))
    _blue_button(style, "Start.TButton", font=(FONT, 22, "bold"), padding=(64, 18))

    # Quiet text-only button (e.g. "Back", "Change").
    style.configure(
        "Link.TButton", background=bg, foreground=settings.ACCENT_COLOR, font=(FONT, 11, "bold"),
        borderwidth=0, focuscolor=bg, lightcolor=bg, darkcolor=bg, bordercolor=bg, padding=(4, 4),
    )
    style.map(
        "Link.TButton",
        background=[("active", bg)],
        foreground=[("active", settings.ACCENT_ACTIVE_COLOR)],
    )

    style.configure("TSpinbox", fieldbackground=panel, foreground=text, arrowcolor=settings.ACCENT_COLOR)

    # One progress bar color per skill, e.g. "speaking.Horizontal.TProgressbar".
    for skill_name, color in settings.SKILL_COLORS.items():
        style.configure(
            f"{skill_name}.Horizontal.TProgressbar",
            background=color, troughcolor=bg, borderwidth=0, lightcolor=color, darkcolor=color,
        )


def _blue_button(style: ttk.Style, name: str, font: tuple, padding: tuple) -> None:
    accent, active = settings.ACCENT_COLOR, settings.ACCENT_ACTIVE_COLOR
    style.configure(
        name, background=accent, foreground=settings.ACCENT_TEXT_COLOR, font=font, padding=padding,
        borderwidth=0, focuscolor=accent, lightcolor=accent, darkcolor=accent, bordercolor=accent,
    )
    style.map(
        name,
        background=[("pressed", active), ("active", active)],
        lightcolor=[("pressed", active), ("active", active)],
        darkcolor=[("pressed", active), ("active", active)],
        bordercolor=[("pressed", active), ("active", active)],
        focuscolor=[("pressed", active), ("active", active)],
    )
