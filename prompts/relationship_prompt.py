import json


def build_relationship_prompt(
    *,
    template_json: dict,
    settings_artifact: dict,
    characters_artifact: dict,
) -> str:
    characters = characters_artifact["characters"]

    victim = None
    detective = None
    suspects = []

    for character in characters:
        roles = set(character.get("roles", []))
        if "victim" in roles:
            victim = character
        elif "detective" in roles:
            detective = character
        elif "suspect" in roles:
            suspects.append(character)

    if victim is None:
        raise ValueError("No victim found in characters artifact.")
    if detective is None:
        raise ValueError("No detective found in characters artifact.")

    expected_relationships = len(suspects) + 1

    return f"""
You are generating intercharacter relationships for a simple murder-mystery story pipeline.

This generator should create ONLY victim-centered relationships.

Generate exactly these pairwise relationships:
- victim ↔ detective
- victim ↔ each suspect

Do NOT generate suspect-suspect relationships.
Do NOT generate detective-suspect relationships.
Do NOT generate any relationships that do not involve the victim.

Important structural rules:
- character_a_id must always be the victim's character_id
- character_b_id must be the other character in the pair
- Return exactly {expected_relationships} relationships total

Narrative guidance:
- All relationships must be grounded in and consistent with the existing character profiles
- Use the world realism level when deciding how dramatic vs restrained the relationships should be
- The detective's relationship to the victim should lean more positive, trusting, respectful, sympathetic, or constructive
- The relationship between the detective and the victim should plausibly provide reasoning for why the detective is trying to solve the murder of the victim
- Suspects' relationships to the victim should lean more negative, strained, resentful, conflicted, distrustful, or emotionally complicated
- The relationships between the suspects and the victim should plausibly provide reasoning for why they may have wanted to murder the victim.
- However, all relationships must still be believable from the profiles; do not force cartoonishly negative or positive dynamics
- The murderer is included among the suspects, so one suspect relationship may be especially tense, hidden, or privately hostile
- Public and private relationship status may differ

Consistency and grounding rules:
- Every relationship must be consistent with the provided character profiles and setting artifact
- Do not include details that contradict a character's background, timeline, role, personality, or established history
- Use only information that is explicit in the profiles or reasonably implied by them
- If a relationship detail is not clearly supported, keep it general rather than specific
- Prefer modest, profile-consistent relationship descriptions over elaborate invented backstory
- Do not turn a weak implication into a concrete fact

When profile support is limited:
- It is acceptable for a relationship to remain somewhat broad, such as polite, distant, tense, familiar, respectful, or strained
- Do not add specific shared history unless the profiles support it

Guidance for fields:
- surface_relationship: the visible/basic relationship label
- public_relationship_status: how others would describe their current relationship
- private_relationship_status: the hidden or emotionally true state of the relationship
- shared_history_summary: how they know each other and what history connects them
- character_a_private_view: how the victim privately views the other character
- character_b_private_view: how the other character privately views the victim
- conflict_level: low, moderate, or high
- trust_level: low, moderate, or high

Settings artifact:
{json.dumps(settings_artifact, indent=2)}

Victim profile:
{json.dumps(victim, indent=2)}

Detective profile:
{json.dumps(detective, indent=2)}

Suspect profiles:
{json.dumps(suspects, indent=2)}

Template shape:
{json.dumps(template_json, indent=2)}

Before producing the final JSON, silently verify for each relationship:
1. No field contradicts either character profile
2. No field adds unsupported concrete facts
3. The overall relationship fits the characters' roles and profiles
If needed, rewrite the relationship in a more general and profile-consistent way.

Output requirements:
- Return valid JSON only
- Match the response schema exactly
- Return exactly {expected_relationships} relationships
- Each relationship must use the victim as character_a_id
- Include exactly one relationship between victim and detective
- Include exactly one relationship between victim and each suspect
""".strip()