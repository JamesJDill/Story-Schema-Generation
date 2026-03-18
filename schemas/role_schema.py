from typing import Literal
from pydantic import BaseModel, Field


class CharacterRoleUpdate(BaseModel):
    character_id: str = Field(description="Existing character ID from characters.json")
    roles: list[Literal["detective", "victim", "suspect", "murderer"]] = Field(
        description="Assigned narrative roles for this character."
    )


class RoleAssignmentArtifact(BaseModel):
    assignments: list[CharacterRoleUpdate]