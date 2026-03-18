import json
import os
from pathlib import Path
from typing import Callable, Type, TypeVar

from google import genai
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def load_json(path: str | Path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_gemini_client(api_key: str | None = None) -> genai.Client:
    """
    Create a reusable Gemini client.

    Priority:
    1. Explicit api_key passed in
    2. GEMINI_API_KEY from environment
    """
    resolved_key = api_key or os.getenv("GEMINI_API_KEY")
    if not resolved_key:
        raise RuntimeError(
            "No Gemini API key found. Pass api_key explicitly or set GEMINI_API_KEY."
        )
    return genai.Client(api_key=resolved_key)


def generate_structured_output(
    *,
    prompt: str,
    schema_model: Type[T],
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.8,
    api_key: str | None = None,
) -> T:
    """
    Generic reusable structured-output generator for Gemini.

    This is intentionally generic so later you can reuse it for:
    - settings
    - character profiles
    - clues / evidence / red herrings
    - relationships
    - role assignments
    """
    client = get_gemini_client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema_model,
            "temperature": temperature,
        },
    )

    raw_text = response.text
    parsed = json.loads(raw_text)

    try:
        return schema_model.model_validate(parsed)
    except ValidationError as e:
        raise RuntimeError(f"Schema validation failed:\n{e}") from e
    

def run_generator(
    *,
    template_path: str | Path,
    prompt_builder: Callable[..., str],
    schema_model: Type[T],
    output_path: str | Path,
    context_artifacts: dict | None = None,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.8,
    api_key: str | None = None,
) -> T:
    """
    Generic orchestration helper for any generator.

    - Loads the generator's template JSON
    - Passes the template plus any upstream artifact context into the prompt builder
    - Calls Gemini with structured output
    - Saves the validated artifact
    """
    template_json = load_json(template_path)
    context_artifacts = context_artifacts or {}

    prompt = prompt_builder(
        template_json=template_json,
        **context_artifacts,
    )

    result = generate_structured_output(
        prompt=prompt,
        schema_model=schema_model,
        model_name=model_name,
        temperature=temperature,
        api_key=api_key,
    )

    save_json(result.model_dump(), output_path)
    return result