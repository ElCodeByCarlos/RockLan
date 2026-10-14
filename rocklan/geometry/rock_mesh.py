from dataclasses import dataclass

import numpy as np

from rocklan.config import settings
from rocklan.geometry.spherical_noise import SphericalNoise


@dataclass
class RockMesh:
    """A closed 3D surface stored as three 2D grids (what matplotlib wants)."""

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray


class RockMeshGenerator:
    """Builds a rock that turns into a perfect sphere as progress goes 0 -> 1.

    Start from a sphere, then deform it in three ways, all scaled by
    `roughness = 1 - progress`:
      1. stretch   - squash/elongate the axes so it isn't round
      2. bumps     - push the surface in and out with SphericalNoise
      3. facets    - slice off flat "chipped" faces
    At progress 1 roughness is 0, so none of them apply: a perfect sphere.
    The seed keeps the rock's shape the same between updates; only the
    strength of the deformations changes, so it looks like it's being polished.
    """

    def __init__(
        self,
        resolution: int = settings.MESH_RESOLUTION,
        max_roughness: float = settings.MAX_ROUGHNESS,
        max_facets: int = settings.MAX_FACETS,
        max_stretch: float = settings.MAX_STRETCH,
        noise_octaves: int = settings.NOISE_OCTAVES,
    ):
        self.resolution = resolution
        self.max_roughness = max_roughness
        self.max_facets = max_facets
        self.max_stretch = max_stretch
        self.noise_octaves = noise_octaves
        self._directions = self._unit_sphere(resolution)

    def generate(self, progress: float, seed: int) -> RockMesh:
        progress = float(np.clip(progress, 0.0, 1.0))
        roughness = 1.0 - progress
        rng = np.random.default_rng(seed)
        directions = self._directions

        noise = SphericalNoise(seed, self.noise_octaves).sample(directions)
        radius = 1.0 + self.max_roughness * roughness * noise
        radius = self._cut_facets(directions, radius, roughness, rng)

        points = directions * radius[..., np.newaxis]
        points *= 1.0 + self.max_stretch * roughness * rng.uniform(-1, 1, size=3)

        # Scale so the farthest point is at distance 1: every rock fills the
        # same space and the final sphere has radius exactly 1.
        points /= np.linalg.norm(points, axis=-1).max()
        return RockMesh(points[..., 0], points[..., 1], points[..., 2])

    def _cut_facets(self, directions, radius, roughness, rng):
        """Flatten the surface wherever it pokes past a random plane."""
        for _ in range(self.max_facets):
            normal = rng.normal(size=3)
            normal /= np.linalg.norm(normal)
            # Always draw the random number so the rock stays stable.
            depth = rng.uniform(0.15, 0.45)
            if roughness == 0.0:
                continue
            plane_distance = 1.0 - depth * roughness
            facing = directions @ normal
            with np.errstate(divide="ignore"):
                limit = np.where(facing > 1e-6, plane_distance / facing, np.inf)
            radius = np.minimum(radius, limit)
        return radius

    @staticmethod
    def _unit_sphere(resolution: int) -> np.ndarray:
        """Grid of unit vectors covering the sphere, shape (rows, cols, 3)."""
        # Start a hair away from the poles: a grid row squeezed into one point
        # has no direction to shade with and shows up as a glitch.
        theta = np.linspace(1e-3, np.pi - 1e-3, resolution)  # top to bottom
        phi = np.linspace(0, 2 * np.pi, resolution * 2)      # around
        theta, phi = np.meshgrid(theta, phi, indexing="ij")
        return np.stack(
            [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)],
            axis=-1,
        )
