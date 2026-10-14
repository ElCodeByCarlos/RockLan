from dataclasses import dataclass

from rocklan.models.skill_type import SkillType


@dataclass
class SkillProgress:
    """Raw progress data for one skill.

    `rock_seed` makes every rock unique but stable: the same seed always
    produces the same rock, so it keeps its identity while it gets smoother.
    """

    skill: SkillType
    xp: int = 0
    rock_seed: int = 0

    def to_dict(self) -> dict:
        return {"skill": self.skill.value, "xp": self.xp, "rock_seed": self.rock_seed}

    @classmethod
    def from_dict(cls, data: dict) -> "SkillProgress":
        return cls(
            skill=SkillType(data["skill"]),
            xp=int(data.get("xp", 0)),
            rock_seed=int(data.get("rock_seed", 0)),
        )
