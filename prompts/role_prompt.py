import json


def build_role_assignment_prompt(
    *,
    template_json: dict,
    settings_artifact: dict,
    characters_artifact: dict,
) -> str:
    suspects = settings_artifact["character_settings"]["suspects"]
    realism_level = settings_artifact["world_settings"]["realism_level"]

    return f"""
You are assigning narrative roles for a murder-mystery story pipeline.

You are given:
1. A settings artifact
2. A characters artifact
3. The output template shape

Your task is to assign story roles to the existing characters based on:
- narrative compellingness
- psychological plausibility
- realism level
- the likely strength of each character as a detective, victim, suspect, or murderer

Important constraints:
- Exactly 1 character must have the role "detective"
- Exactly 1 character must have the role "victim"
- Exactly {suspects} characters must have the role "suspect"
- Exactly 1 character must have the role "murderer"
- The character with role "murderer" must also have role "suspect"
- No character should be both "detective" and "victim"
- No character should be both "detective" and "suspect"
- No character should be both "victim" and "suspect"
- Only the murderer may have two roles: ["suspect", "murderer"]

Realism guidance:
- grounded: assignments should feel restrained, plausible, and psychologically realistic
- slightly heightened: somewhat dramatic, but still believable
- stylized: more theatrical or archetypal choices are acceptable

Role guidance:
- The detective should be someone who can plausibly notice patterns, investigate, or drive discovery
- The victim should be someone whose death creates strong interpersonal consequences
- The murderer should be someone whose profile supports believable motive, concealment, and later revelation
- The suspects should collectively create an interesting and varied suspect pool to craft a compelling story
- The current realism level specified by the settings artifact is {realism_level}. 
- Prioritize plausibility over compellingness accordingness to the realism level specified in the settings artifact: a lesser realism level means to prioritize a more compelling role assignment.

Do not modify the character profiles themselves.
Do not invent new characters.
Only assign roles to the existing character IDs.

Settings artifact:
{json.dumps(settings_artifact, indent=2)}

Characters artifact:
{json.dumps(characters_artifact, indent=2)}

Template shape:
{json.dumps(template_json, indent=2)}

Output requirements:
- Return valid JSON only
- Match the response schema exactly
- Include every character_id exactly once
- Exactly 1 detective
- Exactly 1 victim
- Exactly {suspects} suspects
- Exactly 1 murderer
- The murderer must also be a suspect
""".strip()