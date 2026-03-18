from typing import Literal
from pydantic import BaseModel, Field


class RelationshipEdge(BaseModel):
    character_a_id: str = Field(
        description="Always the victim's character_id for this simplified generator."
    )
    character_b_id: str = Field(
        description="The other character's character_id: either the detective or a suspect."
    )
    surface_relationship: str = Field(
        description="Surface-level relationship label, e.g. friend, employer, niece, neighbor, business partner."
    )
    public_relationship_status: str = Field(
        description="How the relationship appears publicly or is socially understood."
    )
    private_relationship_status: str = Field(
        description="The true private emotional or interpersonal state of the relationship."
    )
    shared_history_summary: str = Field(
        description="Concise summary of the shared past and context between the two characters."
    )
    character_a_private_view: str = Field(
        description="How character_a privately views character_b."
    )
    character_b_private_view: str = Field(
        description="How character_b privately views character_a."
    )
    conflict_level: Literal["low", "moderate", "high"] = Field(
        description="How conflict-heavy the relationship is."
    )
    trust_level: Literal["low", "moderate", "high"] = Field(
        description="How much trust exists in the relationship."
    )


class RelationshipArtifact(BaseModel):
    relationships: list[RelationshipEdge]