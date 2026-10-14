import unittest

import numpy as np

from rocklan.geometry import RockMeshGenerator


def radii(mesh):
    return np.sqrt(mesh.x**2 + mesh.y**2 + mesh.z**2)


class RockMeshTest(unittest.TestCase):
    def setUp(self):
        self.generator = RockMeshGenerator(resolution=24)

    def test_full_progress_is_a_perfect_sphere(self):
        mesh = self.generator.generate(progress=1.0, seed=123)
        np.testing.assert_allclose(radii(mesh), 1.0, atol=1e-9)

    def test_zero_progress_is_rough(self):
        mesh = self.generator.generate(progress=0.0, seed=123)
        self.assertGreater(radii(mesh).std(), 0.05)

    def test_rock_gets_rounder_with_progress(self):
        spreads = [radii(self.generator.generate(p, seed=7)).std() for p in (0.0, 0.5, 0.9)]
        self.assertGreater(spreads[0], spreads[1])
        self.assertGreater(spreads[1], spreads[2])

    def test_same_seed_gives_same_rock(self):
        a = self.generator.generate(0.3, seed=42)
        b = self.generator.generate(0.3, seed=42)
        np.testing.assert_array_equal(a.x, b.x)


if __name__ == "__main__":
    unittest.main()
