# RockLan

Learn a language and watch your progress take shape: each of the four skills
(**speaking, writing, listening, reading**) is a 3D rock. As you log
practice, the rock is "polished" until it becomes a perfect sphere at
mastery.

## Run it

```powershell
py -m pip install -r requirements.txt   # numpy + matplotlib (tkinter ships with Python)
py main.py            # your real profile, saved to data/profile.json
py main.py --demo     # rocks at 0 / 33 / 66 / 100 %, nothing saved
py -m unittest discover -s tests -t .   # run the tests
```

Press **Start**, pick one of the four skills, and log practice on its page.
Drag the rock with the mouse to rotate it.

## How the code is organized

```
main.py                     entry point (reads --demo, calls app.run)
rocklan/
  app.py                    builds every piece and connects them
  config/settings.py        ALL tweakable numbers & colors
  models/                   plain data, no logic
    skill_type.py             SkillType enum (the 4 skills)
    skill_progress.py         xp + rock_seed for one skill
    learner_profile.py        target language + the 4 SkillProgress
  progress/                 the rules
    level_calculator.py       XP -> progress (0..1) and CEFR level (A1..C2)
    progress_tracker.py       the ONLY place progress changes (log practice, save)
  storage/
    profile_repository.py     load/save the profile as JSON
  geometry/                 3D math, no UI
    spherical_noise.py        smooth random bumps on a sphere
    rock_mesh.py              RockMeshGenerator: progress -> rock surface
  ui/                       what you see
    main_window.py            switches screens: Start -> Home -> Skill page
    start_screen.py           first screen: title + big blue Start button
    home_screen.py            4 clickable skill cards (one per category)
    skill_screen.py           one skill's page: its rock + practice controls
    rock_view.py              one matplotlib 3D rock
    practice_controls.py      level, progress bar + "log practice" input
    language_dialog.py        scrollable language picker (list in settings.LANGUAGES)
    theme.py                  light-blue ttk styles
tests/                      unit tests for geometry and progress rules
```

**Data flow when you click "Log practice":**
`PracticeControls` -> `SkillScreen._log_practice` -> `ProgressTracker.log_practice`
(adds XP, saves JSON) -> `SkillScreen._refresh` -> `RockView.show`
(asks `RockMeshGenerator` for a new mesh and draws it).

**How the rock becomes a sphere** (`geometry/rock_mesh.py`): start from a
sphere and apply three deformations (stretch, noise bumps, flat facets),
all multiplied by `roughness = 1 - progress`. At 100% roughness is 0, so
it is an exact sphere. Each skill has a fixed `rock_seed`, so the rock keeps
its identity and only gets smoother.

## Recipes for changing things

| I want to...                            | Edit                                                          |
|-----------------------------------------|---------------------------------------------------------------|
| Make mastery take more/less time        | `MAX_XP` / `XP_PER_MINUTE` in `config/settings.py`            |
| Make rocks rougher or smoother          | `MAX_ROUGHNESS`, `MAX_FACETS`, `MAX_STRETCH` in settings      |
| Add / remove pickable languages         | `LANGUAGES` in `config/settings.py`                           |
| Change colors (e.g. the blue accent)    | `ACCENT_COLOR`, `BACKGROUND_COLOR`, `SKILL_COLORS`, ... in settings |
| Change level names / thresholds         | `CEFR_LEVELS` in `progress/level_calculator.py`               |
| Give XP for other things (quizzes, ...) | add a method to `ProgressTracker`, call it from the UI        |
| Add a 5th skill                         | add it to `SkillType`, add its color to `SKILL_COLORS`, and the card grid in `home_screen.py` adapts (2 per row) |
| Save to a database instead of JSON      | new class with `load()`/`save()` like `ProfileRepository`, pass it in `app.py` |
| Swap matplotlib for a real 3D engine    | only `ui/rock_view.py` changes; `RockMeshGenerator` already gives you x/y/z grids |

Rule of thumb: **models** hold data, **progress** holds rules, **geometry**
holds math, **ui** only displays and forwards clicks. Keeping those apart
is what lets you change one without breaking the others.
