import tempfile
import unittest
from pathlib import Path

from rocklan.models import LearnerProfile, SkillType
from rocklan.progress import LevelCalculator, ProgressTracker
from rocklan.storage import ProfileRepository


class LevelCalculatorTest(unittest.TestCase):
    def setUp(self):
        self.calculator = LevelCalculator(max_xp=600)

    def test_progress_is_clamped(self):
        self.assertEqual(self.calculator.progress(-5), 0.0)
        self.assertEqual(self.calculator.progress(300), 0.5)
        self.assertEqual(self.calculator.progress(9999), 1.0)

    def test_levels(self):
        self.assertEqual(self.calculator.level(0), "A1")
        self.assertEqual(self.calculator.level(300), "B2")
        self.assertEqual(self.calculator.level(600), "Mastery")


class ProgressTrackerTest(unittest.TestCase):
    def test_log_practice_adds_xp_and_saves(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = ProfileRepository(Path(folder) / "profile.json")
            tracker = ProgressTracker(LearnerProfile.new("French"), LevelCalculator(600), repository)

            tracker.log_practice(SkillType.READING, 45)

            loaded = repository.load()
            self.assertEqual(loaded.target_language, "French")
            self.assertEqual(loaded.get(SkillType.READING).xp, 45)
            self.assertEqual(loaded.get(SkillType.SPEAKING).xp, 0)

    def test_xp_never_exceeds_max(self):
        tracker = ProgressTracker(LearnerProfile.new("German"), LevelCalculator(100))
        tracker.log_practice(SkillType.WRITING, 500)
        self.assertEqual(tracker.profile.get(SkillType.WRITING).xp, 100)


if __name__ == "__main__":
    unittest.main()
