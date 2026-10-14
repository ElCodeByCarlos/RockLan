from enum import Enum


class SkillType(Enum):
    """The four language skills. Each one gets its own rock."""

    SPEAKING = "speaking"
    WRITING = "writing"
    LISTENING = "listening"
    READING = "reading"

    @property
    def label(self) -> str:
        return self.value.capitalize()
