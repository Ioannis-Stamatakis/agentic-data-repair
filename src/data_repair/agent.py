"""Pydantic AI agent for intelligent data repair."""

import os
from pathlib import Path
from pydantic_ai import Agent
from .schemas import SalesLead

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not installed, rely on environment


# Initialize agent with Gemini Flash and structured output
repair_agent = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=SalesLead,
    system_prompt=(
        "You are a Data Repair Expert specializing in sales lead quality.\n\n"
        "Your task: Fix invalid sales lead data to match the strict schema.\n\n"
        "Rules:\n"
        "1. Normalize country names to ISO 3166-1 alpha-2 codes:\n"
        "   - 'United States', 'USA', 'usa' → 'US'\n"
        "   - 'United Kingdom', 'uk', 'england' → 'GB'\n"
        "   - 'Germany', 'deutschland', 'germany' → 'DE'\n"
        "   - 'Japan', 'nippon' → 'JP'\n"
        "   - 'France' → 'FR'\n"
        "   - 'Australia' → 'AU'\n"
        "   - 'Canada' → 'CA'\n"
        "   - 'Spain', 'españa' → 'ES'\n"
        "   - 'Russia' → 'RU'\n"
        "2. Convert names to Title Case (e.g., 'john smith' → 'John Smith', 'BOB MARLEY' → 'Bob Marley')\n"
        "3. Fix email formatting (lowercase, proper domain)\n"
        "4. Infer segment from contract value if missing or invalid:\n"
        "   - $100,000+ → Enterprise\n"
        "   - $25,000-$99,999 → Mid-Market\n"
        "   - <$25,000 → SMB\n"
        "5. Map segment variations:\n"
        "   - 'small business', 'smb', 'small' → SMB\n"
        "   - 'enterprise', 'large' → Enterprise\n"
        "   - 'mid-market', 'medium', 'midmarket' → Mid-Market\n"
        "6. Clean contract values: Remove '$', commas, convert to float\n"
        "7. NEVER invent personal data (names, emails) - fail gracefully if data is missing\n\n"
        "Return a fully valid SalesLead object or raise an error if impossible."
    )
)


def repair_lead(invalid_row: dict, validation_error: str) -> SalesLead:
    """Attempt to repair an invalid lead using the AI agent.

    Args:
        invalid_row: Dictionary with invalid data
        validation_error: Pydantic validation error message

    Returns:
        Repaired SalesLead object with all validations passing

    Raises:
        Exception: If repair is impossible (e.g., missing critical data)
    """
    prompt = (
        f"Original data: {invalid_row}\n\n"
        f"Validation error: {validation_error}\n\n"
        "Please fix this data to match the SalesLead schema."
    )

    result = repair_agent.run_sync(prompt)
    return result.output
