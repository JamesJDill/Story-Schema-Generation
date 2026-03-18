from typing import Literal
from pydantic import BaseModel, Field


class PhysicalTraits(BaseModel):
    name: str = Field(description="Full character name.")
    age: int = Field(ge=12, le=95, description="Character age.")
    sex: str = Field(description="Character sex.")
    sexual_orientation: str = Field(description="Character sexual orientation.")
    height: str = Field(description='Character height in a natural format, e.g. 5\'10".')
    weight: str = Field(description="Character weight in a natural format.")
    build: str = Field(description="Physical build, e.g. lean, broad-shouldered, wiry.")


class SocialProfile(BaseModel):
    occupation: str = Field(description="Character occupation or primary social role.")
    wealth_status: str = Field(description="Character wealth or class status.")
    education: str = Field(description="Character education level or background.")


class Background(BaseModel):
    origin: str = Field(description="Where the character comes from.")
    personal_history_summary: str = Field(
        description="A concise summary of the character's personal history."
    )
    notable_past_events: list[str] = Field(
        description="Important events from the character's past."
    )


class Personality(BaseModel):
    core_traits: list[str] = Field(description="Core personality traits.")
    outward_demeanor: str = Field(description="How the character presents outwardly.")
    inner_conflicts: list[str] = Field(description="Internal struggles or contradictions.")


class Behaviors(BaseModel):
    speech_pattern: str = Field(description="How the character tends to speak.")
    lying_tells: str = Field(description="Behavioral tells shown when lying.")
    habits: list[str] = Field(description="Recurring habits or routines.")


class GeneratedCharacterProfile(BaseModel):
    physical_traits: PhysicalTraits
    social_profile: SocialProfile
    background: Background
    personality: Personality
    behaviors: Behaviors


class CharacterProfile(GeneratedCharacterProfile):
    character_id: str = Field(description="Stable unique identifier like char_01, char_02, etc.")
    roles: list[Literal["detective", "victim", "suspect", "murderer"]] = Field(
        default_factory=list,
        description="Narrative roles assigned in a later stage."
    )


class CharacterArtifactLLM(BaseModel):
    characters: list[GeneratedCharacterProfile]


class CharacterArtifact(BaseModel):
    characters: list[CharacterProfile]