from typing import Literal
from pydantic import BaseModel, Field


class MotiveEntry(BaseModel):
    character_id: str = Field(
        description="The character receiving the motive. Must be a detective or suspect, never the victim."
    )
    character_role: Literal["detective", "suspect"] = Field(
        description="The story role of the character receiving the motive."
    )
    motive_type: Literal["positive", "negative"] = Field(
        description="Positive for the detective's truth-seeking motive, negative for suspects' harmful motives."
    )
    motive_summary: str = Field(
        description="Concise explanation of the character's motive."
    )
    target_character_id: str = Field(
        description="Always the victim's character_id for this simplified generator."
    )
    motive_strength: Literal["low", "moderate", "high"] = Field(
        description="How strong or intense the motive is."
    )
    is_red_herring: Literal["true", "false"] = Field(
        description="False for the detective and actual murderer, true for innocent suspects."
    )


class MotiveArtifact(BaseModel):
    motives: list[MotiveEntry]