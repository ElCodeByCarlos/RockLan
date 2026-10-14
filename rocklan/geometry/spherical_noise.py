import numpy as np


class SphericalNoise:
    """Smooth, seamless random bumps over the surface of a sphere.

    It adds up sine waves pointing in random 3D directions. Each "octave"
    doubles the frequency (smaller bumps) and halves the strength, which is
    what gives rocks big lumps with small details on top.
    Because it works on 3D points, there are no seams or pinched poles.
    """

    WAVES_PER_OCTAVE = 6

    def __init__(self, seed: int, octaves: int = 5):
        rng = np.random.default_rng(seed)
        directions, phases, amplitudes = [], [], []
        for octave in range(octaves):
            frequency = 1.5 * 2**octave
            amplitude = 0.5**octave
            for _ in range(self.WAVES_PER_OCTAVE):
                direction = rng.normal(size=3)
                directions.append(direction / np.linalg.norm(direction) * frequency)
                phases.append(rng.uniform(0, 2 * np.pi))
                amplitudes.append(amplitude)
        self._directions = np.array(directions)     # (waves, 3)
        self._phases = np.array(phases)             # (waves,)
        self._amplitudes = np.array(amplitudes)     # (waves,)

    def sample(self, points: np.ndarray) -> np.ndarray:
        """Return a value in [-1, 1] for each point. `points` has shape (..., 3)."""
        waves = np.sin(points @ self._directions.T + self._phases)  # (..., waves)
        return (waves @ self._amplitudes) / self._amplitudes.sum()
