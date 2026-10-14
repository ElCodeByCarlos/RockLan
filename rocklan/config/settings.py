"""Tweakable values for the whole app.

Change numbers here instead of hunting through the code.
"""
from pathlib import Path

# ---------------------------------------------------------------- files
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROFILE_FILE = DATA_DIR / "profile.json"

# ------------------------------------------------------------- progress
XP_PER_MINUTE = 1
# XP a single skill needs to become a perfect sphere (6000 = 100 hours).
MAX_XP = 6000

# ---------------------------------------------------------- rock shape
MESH_RESOLUTION = 48   # rows in the sphere grid (columns = 2 x rows)
MAX_ROUGHNESS = 0.55   # how bumpy the rock is at 0% progress
MAX_FACETS = 9         # flat "chipped" faces at 0% progress
MAX_STRETCH = 0.30     # how elongated/squashed the rock is at 0% progress
NOISE_OCTAVES = 5      # layers of detail in the bumps

# --------------------------------------------------------------- colors
BACKGROUND_COLOR = "#e8f5fe"     # very light blue page background
PANEL_COLOR = "#ffffff"          # cards and side panels
BORDER_COLOR = "#c9e4f8"         # card outlines
TEXT_COLOR = "#1b3a57"           # dark navy, readable on light blue
MUTED_TEXT_COLOR = "#5b7a95"
ACCENT_COLOR = "#38a3f1"         # the main light blue (buttons, highlights)
ACCENT_ACTIVE_COLOR = "#1f8fe0"  # buttons while hovered / pressed
ACCENT_TEXT_COLOR = "#ffffff"    # text on top of ACCENT_COLOR
ROCK_BASE_COLOR = "#6b6560"      # raw stone; blends into the skill color

# Keys match SkillType values (see models/skill_type.py).
SKILL_COLORS = {
    "speaking": "#e07a5f",
    "writing": "#f2cc8f",
    "listening": "#81b29a",
    "reading": "#6c9bd2",
}

# ------------------------------------------------------------ languages
# Choices in the scrollable language picker (add or remove freely).
LANGUAGES = [
    "Arabic", "Bengali", "Catalan", "Chinese (Mandarin)", "Czech", "Danish", "Dutch",
    "English", "Finnish", "French", "German", "Greek", "Hebrew", "Hindi", "Hungarian",
    "Indonesian", "Italian", "Japanese", "Korean", "Norwegian", "Persian", "Polish",
    "Portuguese", "Romanian", "Russian", "Spanish", "Swahili", "Swedish", "Thai",
    "Turkish", "Ukrainian", "Vietnamese",
]

# -------------------------------------------------------------- window
WINDOW_TITLE = "RockLan"
WINDOW_SIZE = "1150x760"
