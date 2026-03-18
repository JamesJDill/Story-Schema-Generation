
from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class StorySettings(BaseModel):
    sub_genre: str = Field(description="Specific mystery subgenre, e.g. cozy mystery, noir detective, police procedural")
    intended_audience: str = Field(description="Target audience, e.g. adult, young adult, teen, pre-teen.")
    writing_style: str = Field(description="Narrative style, e.g. atmospheric, witty, fast-paced, literary, old english shakespearean.")
    reading_level: str = Field(description="Reading difficulty, e.g. middle school, high school, adult general.")
    point_of_view: str = Field(description="Narrative POV, e.g. first person, third person limited, third person omniscient.")
    
    
class WorldSettings(BaseModel):
    time_period: str = Field(description="Time period in which the story takes place.")
    location: str = Field(description="Primary setting/location of the story.")
    realism_level: Literal["grounded", "slightly heightened", "stylized"] = Field(
        description="How realistic the world should feel."
    )
    
    
class CharacterSettings(BaseModel):
    complexity: Literal["simple", "moderate", "complex"] = Field(
        description="How psychologically and developmentally complex the characters and their relationships, personalities, and backgrounds should be."
    )
    suspects: int = Field(ge=2, le=10, description="Number of suspects. Must be at least 2.")
    
    
class Settings(BaseModel):
    story_settings: StorySettings
    world_settings: WorldSettings
    character_settings: CharacterSettings