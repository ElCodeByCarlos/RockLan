import random
from dataclasses import dataclass, field

from rocklan.models.skill_progress import SkillProgress
from rocklan.models.skill_type import SkillType


@dataclass
class LearnerProfile:
    """Everything we know about the learner: target language + 4 skills."""

    target_language: str
    skills: dict[SkillType, SkillProgress] = field(default_factory=dict)

    @classmethod
    def new(cls, target_language: str, rng: random.Random | None = None) -> "LearnerProfile":
        """Create a fresh profile where every skill gets its own random rock."""
        rng = rng or random.Random()
        skills = {
            skill: SkillProgress(skill=skill, rock_seed=rng.randrange(2**31))
            for skill in SkillType
        }
        return cls(target_language=target_language, skills=skills)

    def get(self, skill: SkillType) -> SkillProgress:
        return self.skills[skill]

    def to_dict(self) -> dict:
        return {
            "target_language": self.target_language,
            "skills": [progress.to_dict() for progress in self.skills.values()],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LearnerProfile":
        profile = cls.new(data.get("target_language", ""))
        # Saved skills override the defaults; missing ones keep a new rock.
        for item in data.get("skills", []):
            progress = SkillProgress.from_dict(item)
            profile.skills[progress.skill] = progress
        return profile
