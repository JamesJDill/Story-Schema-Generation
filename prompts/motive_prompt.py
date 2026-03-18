import json


def build_motive_prompt(
    *,
    template_json: dict,
    settings_artifact: dict,
    characters_artifact: dict,
    relationships_artifact: dict,
) -> str:
    characters = characters_artifact["characters"]
    relationships = relationships_artifact["relationships"]

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

    victim_id = victim["character_id"]

    detective_relationship = None
    suspect_relationships = []

    for relationship in relationships:
        if relationship.get("character_a_id") != victim_id:
            continue

        other_id = relationship.get("character_b_id")

        if other_id == detective["character_id"]:
            detective_relationship = relationship
            continue

        for suspect in suspects:
            if suspect["character_id"] == other_id:
                suspect_relationships.append(
                    {
                        "suspect_profile": suspect,
                        "relationship_to_victim": relationship,
                    }
                )
                break

    if detective_relationship is None:
        raise ValueError("No victim-detective relationship found in relationships artifact.")

    if len(suspect_relationships) != len(suspects):
        raise ValueError(
            "Relationships artifact does not contain exactly one victim-centered relationship for each suspect."
        )

    expected_motives = len(suspects) + 1

    return f"""
You are generating character motives for a simple murder-mystery story pipeline.

Generate motives for every non-victim character:
- exactly one motive for the detective
- exactly one motive for each suspect

Do NOT generate a motive for the victim.
Do NOT generate multiple motives for the same character.

Important structural rules:
- character_id must be the character receiving the motive
- character_role must be either "detective" or "suspect"
- target_character_id must always be the victim's character_id
- Return exactly {expected_motives} motives total

Narrative guidance:
- All motives must be grounded in and consistent with the existing character profiles, roles, relationships, and setting
- Use the world realism level when deciding how dramatic vs restrained the motives should be
- The detective's motive should explain why they want to uncover the truth of the murder
- The detective's motive should be constructive, truth-seeking, justice-oriented, protective, dutiful, or personally meaningful in a positive way
- Suspects' motives should explain why they may have wanted the victim dead
- Suspects' motives should lean more negative, such as resentment, fear, jealousy, anger, shame, self-protection, financial pressure, status anxiety, buried grievance, or other believable harmful motive
- The murderer is included among the suspects, so one suspect motive may be especially strong, deeply personal, or closely tied to the central conflict
- However, all motives must still be believable from the profiles and relationships; do not force melodramatic or unsupported motives

Role-specific rules:
- The detective must have:
  - character_role = "detective"
  - motive_type = "positive"
  - is_red_herring = "false"
- Every suspect must have:
  - character_role = "suspect"
  - motive_type = "negative"
- The actual murderer should have:
  - is_red_herring = "false"
- Every suspect who is not the murderer should have:
  - is_red_herring = "true"

Consistency and grounding rules:
- Every motive must be consistent with the provided character profiles, relationship data, and setting artifact
- Do not include details that contradict a character's background, timeline, role, personality, or established history
- Use only information that is explicit in the artifacts or reasonably implied by them
- If a motive detail is not clearly supported, keep it general rather than specific
- Prefer modest, profile-consistent motives over elaborate invented backstory
- Do not turn a weak implication into a concrete fact

When artifact support is limited:
- It is acceptable for a motive to remain somewhat broad rather than highly specific
- Do not add secret incidents, financial arrangements, betrayals, blackmail, threats, or past confrontations unless the artifacts support them

Guidance for fields:
- character_id: the character receiving the motive
- character_role: detective or suspect
- motive_type:
  - positive for the detective
  - negative for suspects
- motive_summary:
  - concise summary of the character's motive
  - for the detective, explain why they want to solve the murder
  - for suspects, explain why they may have wanted the victim dead
- target_character_id: always the victim's character_id
- motive_strength: low, moderate, or high
- is_red_herring:
  - false for the detective
  - false for the murderer
  - true for innocent suspects

Settings artifact:
{json.dumps(settings_artifact, indent=2)}

Victim profile:
{json.dumps(victim, indent=2)}

Detective profile:
{json.dumps(detective, indent=2)}

Detective relationship to victim:
{json.dumps(detective_relationship, indent=2)}

Suspect profiles and relationships to victim:
{json.dumps(suspect_relationships, indent=2)}

Template shape:
{json.dumps(template_json, indent=2)}

Before producing the final JSON, silently verify for each motive:
1. The motive matches the character's role
2. The motive does not contradict the character profile or relationship
3. The motive_type is correct for that role
4. The target_character_id is the victim's character_id
5. is_red_herring is correct for the character's role assignment
If needed, rewrite the motive in a more general and profile-consistent way.

Output requirements:
- Return valid JSON only
- Match the response schema exactly
- Return exactly {expected_motives} motives
- Include exactly one detective motive
- Include exactly one motive for each suspect
""".strip()