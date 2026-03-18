import json


def build_character_prompt(*, template_json: dict, settings_artifact: dict) -> str:
    suspects = settings_artifact["character_settings"]["suspects"]
    total_characters = suspects + 2

    story_settings = settings_artifact["story_settings"]
    world_settings = settings_artifact["world_settings"]
    character_settings = settings_artifact["character_settings"]

    return f"""
You are generating a cast of character profiles for a murder-mystery story generation pipeline.

This stage is ONLY responsible for generating plausible, distinct, fully formed character profiles.
Do NOT assign final causal roles such as detective, victim, suspect, or murderer.
Those role assignments will happen later.

You must generate exactly {total_characters} character profiles because the later story pipeline requires:
- 1 detective
- 1 victim
- {suspects} suspects

Your task is to produce a cast pool that could later support those roles.

Requirements:
- Every character must feel distinct in name, personality, background, behavior, and social position.
- Characters should fit the setting, tone, realism level, and intended audience.
- Use the realism level to guide how grounded or stylized the characters are allowed to be.
- Use the character complexity setting to determine how layered their psychology, history, contradictions, and habits should be.
- Characters should be plausible within the world and capable of participating in motives, secrets, conflict, clues, and red herrings later.
- Avoid duplicates or near-duplicates.
- Avoid assigning explicit final story roles.
- Do not include character IDs. IDs will be assigned by the system after generation.

Character diversity guidance:
- Vary names, ages, occupations, wealth status, education, and social standing where appropriate.
- Vary speech patterns, habits, and internal conflicts.
- Make sure different characters have different social energies and histories.
- Keep the cast cohesive to the setting rather than random.

Setting context:
Story settings:
{json.dumps(story_settings, indent=2)}

World settings:
{json.dumps(world_settings, indent=2)}

Character settings:
{json.dumps(character_settings, indent=2)}

Characters artifact template shape:
{json.dumps(template_json, indent=2)}

Output requirements:
- Return valid JSON only.
- Output must match the response schema exactly.
- Include exactly {total_characters} entries in characters.
""".strip()