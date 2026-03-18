def assign_character_ids(characters_result):
    from schemas.character_schema import CharacterArtifact, CharacterProfile

    final_characters = []
    for i, character in enumerate(characters_result.characters, start=1):
        final_characters.append(
            CharacterProfile(
                character_id=f"char_{i:02d}",
                **character.model_dump()
            )
        )

    return CharacterArtifact(characters=final_characters)


def assign_roles_to_characters(characters_result, role_assignment_result):
    from schemas.character_schema import CharacterArtifact, CharacterProfile
    from schemas.role_schema import RoleAssignmentArtifact

    if isinstance(characters_result, dict):
        characters_result = CharacterArtifact.model_validate(characters_result)

    if isinstance(role_assignment_result, dict):
        role_assignment_result = RoleAssignmentArtifact.model_validate(role_assignment_result)

    role_map = {}
    for assignment in role_assignment_result.assignments:
        if assignment.character_id in role_map:
            raise ValueError(f"Duplicate role assignment for {assignment.character_id}")
        role_map[assignment.character_id] = assignment.roles

    character_ids = {c.character_id for c in characters_result.characters}
    assignment_ids = set(role_map.keys())

    if character_ids != assignment_ids:
        raise ValueError(
            f"Character IDs and assignment IDs do not match.\n"
            f"characters={sorted(character_ids)}\n"
            f"assignments={sorted(assignment_ids)}"
        )

    detective_count = 0
    victim_count = 0
    suspect_count = 0
    murderer_count = 0

    for cid, roles in role_map.items():
        role_set = set(roles)

        if "detective" in role_set:
            detective_count += 1
        if "victim" in role_set:
            victim_count += 1
        if "suspect" in role_set:
            suspect_count += 1
        if "murderer" in role_set:
            murderer_count += 1
            if "suspect" not in role_set:
                raise ValueError(f"{cid} is murderer but not suspect.")

        if "detective" in role_set and "victim" in role_set:
            raise ValueError(f"{cid} cannot be both detective and victim.")
        if "detective" in role_set and "suspect" in role_set:
            raise ValueError(f"{cid} cannot be both detective and suspect.")
        if "victim" in role_set and "suspect" in role_set:
            raise ValueError(f"{cid} cannot be both victim and suspect.")

    updated_characters = []
    for character in characters_result.characters:
        updated_characters.append(
            CharacterProfile(
                **character.model_dump(exclude={"roles"}),
                roles=role_map[character.character_id],
            )
        )

    return CharacterArtifact(characters=updated_characters)


def validate_relationships_artifact(relationships_artifact, characters_artifact):
    from schemas.relationship_schema import RelationshipArtifact
    from schemas.character_schema import CharacterArtifact

    if isinstance(relationships_artifact, dict):
        relationships_artifact = RelationshipArtifact.model_validate(relationships_artifact)

    if isinstance(characters_artifact, dict):
        characters_artifact = CharacterArtifact.model_validate(characters_artifact)

    victim_id = None
    detective_id = None
    suspect_ids = []

    for character in characters_artifact.characters:
        roles = set(character.roles)
        if "victim" in roles:
            victim_id = character.character_id
        elif "detective" in roles:
            detective_id = character.character_id
        elif "suspect" in roles:
            suspect_ids.append(character.character_id)

    if victim_id is None:
        raise ValueError("No victim found in characters artifact.")
    if detective_id is None:
        raise ValueError("No detective found in characters artifact.")

    expected_pairs = {(victim_id, detective_id)}
    for suspect_id in suspect_ids:
        expected_pairs.add((victim_id, suspect_id))

    actual_pairs = set()
    for rel in relationships_artifact.relationships:
        pair = (rel.character_a_id, rel.character_b_id)
        if pair in actual_pairs:
            raise ValueError(f"Duplicate relationship pair: {pair}")
        actual_pairs.add(pair)

    if actual_pairs != expected_pairs:
        raise ValueError(
            f"Relationship pairs do not match expected victim-centered pairs.\n"
            f"Expected: {sorted(expected_pairs)}\n"
            f"Actual: {sorted(actual_pairs)}"
        )

    return relationships_artifact

def validate_motives_artifact(motives_artifact, characters_artifact):
    from schemas.motive_schema import MotiveArtifact
    from schemas.character_schema import CharacterArtifact

    if isinstance(motives_artifact, dict):
        motives_artifact = MotiveArtifact.model_validate(motives_artifact)

    if isinstance(characters_artifact, dict):
        characters_artifact = CharacterArtifact.model_validate(characters_artifact)

    victim_id = None
    detective_id = None
    suspect_ids = []
    murderer_ids = set()

    characters_by_id = {}

    for character in characters_artifact.characters:
        characters_by_id[character.character_id] = character
        roles = set(character.roles)

        if "victim" in roles:
            victim_id = character.character_id
        elif "detective" in roles:
            detective_id = character.character_id
        elif "suspect" in roles:
            suspect_ids.append(character.character_id)

        if "murderer" in roles:
            murderer_ids.add(character.character_id)

    if victim_id is None:
        raise ValueError("No victim found in characters artifact.")
    if detective_id is None:
        raise ValueError("No detective found in characters artifact.")

    expected_character_ids = {detective_id, *suspect_ids}
    actual_character_ids = set()

    for motive in motives_artifact.motives:
        if motive.character_id in actual_character_ids:
            raise ValueError(f"Duplicate motive for character_id: {motive.character_id}")
        actual_character_ids.add(motive.character_id)

        if motive.character_id == victim_id:
            raise ValueError("Victim should not have a motive entry.")

        if motive.target_character_id != victim_id:
            raise ValueError(
                f"Motive target_character_id must always be the victim_id '{victim_id}', "
                f"but got '{motive.target_character_id}' for character '{motive.character_id}'."
            )

        if motive.character_id not in characters_by_id:
            raise ValueError(f"Unknown character_id in motives artifact: {motive.character_id}")

        roles = set(characters_by_id[motive.character_id].roles)

        if "detective" in roles:
            if motive.character_role != "detective":
                raise ValueError(
                    f"Character '{motive.character_id}' should have character_role='detective'."
                )
            if motive.motive_type != "positive":
                raise ValueError(
                    f"Detective '{motive.character_id}' must have motive_type='positive'."
                )
            if motive.is_red_herring != "false":
                raise ValueError(
                    f"Detective '{motive.character_id}' must have is_red_herring='false'."
                )

        elif "suspect" in roles:
            if motive.character_role != "suspect":
                raise ValueError(
                    f"Character '{motive.character_id}' should have character_role='suspect'."
                )
            if motive.motive_type != "negative":
                raise ValueError(
                    f"Suspect '{motive.character_id}' must have motive_type='negative'."
                )

            expected_red_herring = "false" if "murderer" in roles else "true"
            if motive.is_red_herring != expected_red_herring:
                raise ValueError(
                    f"Suspect '{motive.character_id}' has incorrect is_red_herring value. "
                    f"Expected '{expected_red_herring}', got '{motive.is_red_herring}'."
                )
        else:
            raise ValueError(
                f"Character '{motive.character_id}' is neither detective nor suspect."
            )

    if actual_character_ids != expected_character_ids:
        raise ValueError(
            f"Motive character_ids do not match expected non-victim characters.\n"
            f"Expected: {sorted(expected_character_ids)}\n"
            f"Actual: {sorted(actual_character_ids)}"
        )

    return motives_artifact