import json

def build_settings_prompt(template_json: dict) -> str:
    return f"""
You are generating the initial settings artifact for a murder-mystery story generation pipeline.

Your job is to fill in every empty field in the provided JSON template with coherent, internally consistent values.

Requirements:
- This is for a mystery/crime story pipeline.
- The generated settings must support downstream creation of:
  - exactly 1 detective
  - exactly 1 victim
  - exactly N suspects, where N = character_settings.suspects
  - exactly 1 true murderer, chosen from among the suspects
- Choose values that make future clue generation, red herrings, motives, and relationships plausible.
- Keep the setting vivid and specific, but not so restrictive that later generators lose flexibility.
- Prefer clean, practical values over overly quirky ones.

Guidance:
- sub_genre examples: cozy mystery, locked-room mystery, noir detective, police procedural, campus mystery
- intended_audience examples: adult, young adult, teen
- writing_style examples: atmospheric, witty, suspenseful, literary, brisk
- reading_level examples: middle school, high school, adult general
- point_of_view examples: first person, third person limited, third person omniscient
- realism_level must be one of: grounded, slightly heightened, stylized
- complexity must be one of: simple, moderate, complex
- suspects must be an integer between 2 and 10

Return only the completed JSON object.

Input template:
{json.dumps(template_json, indent=2)}
""".strip()