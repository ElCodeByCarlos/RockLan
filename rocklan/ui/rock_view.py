import tkinter as tk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LightSource, to_rgb
from matplotlib.figure import Figure

from rocklan.config import settings
from rocklan.geometry import RockMeshGenerator
from rocklan.models import SkillType


def blend(color_a: str, color_b: str, amount: float) -> tuple[float, float, float]:
    """Mix two colors. amount=0 gives color_a, amount=1 gives color_b."""
    a, b = np.array(to_rgb(color_a)), np.array(to_rgb(color_b))
    return tuple(a + (b - a) * amount)


class RockView:
    """One big 3D rock. Drag it to rotate."""

    def __init__(self, parent: tk.Widget, generator: RockMeshGenerator):
        self.generator = generator
        self.figure = Figure(figsize=(6, 6), facecolor=settings.BACKGROUND_COLOR)
        self.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().configure(background=settings.BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._light = LightSource(azdeg=315, altdeg=35)
        self._ax = self.figure.add_subplot(projection="3d")

    def show(self, skill: SkillType, progress: float, seed: int) -> None:
        ax = self._ax
        elev, azim = ax.elev, ax.azim  # keep the user's rotation across redraws
        ax.clear()

        mesh = self.generator.generate(progress, seed)
        color = blend(settings.ROCK_BASE_COLOR, settings.SKILL_COLORS[skill.value], progress)
        ax.plot_surface(
            mesh.x, mesh.y, mesh.z,
            color=color, shade=True, lightsource=self._light,
            rstride=1, cstride=1, linewidth=0, antialiased=False,
        )

        ax.set_box_aspect((1, 1, 1), zoom=1.2)
        for set_limit in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
            set_limit(-1, 1)
        ax.set_axis_off()
        ax.set_facecolor(settings.BACKGROUND_COLOR)
        ax.view_init(elev=elev, azim=azim)
        self.canvas.draw_idle()
