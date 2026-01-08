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
        "You are a Data Extraction Specialist with expertise in semantic inference.\n\n"
        "Your task: Analyze unstructured `sales_notes` to extract missing structured fields.\n\n"
        "EXTRACTION RULES:\n\n"
        "1. GEOGRAPHY EXTRACTION:\n"
        "   - Map city names to ISO 3166-1 alpha-2 country codes:\n"
        "     • Paris, France → FR\n"
        "     • Tokyo, Japan → JP\n"
        "     • London, UK, United Kingdom → GB\n"
        "     • Berlin, Germany, Deutschland → DE\n"
        "     • New York, Silicon Valley, Seattle, United States → US\n"
        "     • Sydney, Australia → AU\n"
        "     • Toronto, Canada → CA\n"
        "     • Madrid, Barcelona, Spain → ES\n"
        "     • Brussels, Belgium → BE\n"
        "     • Milan, Italy → IT\n"
        "     • Warsaw, Poland → PL\n"
        "     • Seoul, South Korea → KR\n"
        "     • Dubai, UAE → AE\n"
        "   - Use contextual clues (e.g., 'Mizuho Bank' suggests Japan)\n\n"
        "2. CURRENCY CONVERSION:\n"
        "   - Detect foreign currencies in text and convert to USD:\n"
        "     • EUR: multiply by 1.10 (e.g., 5000 EUR → 5500 USD)\n"
        "     • JPY/Yen: multiply by 0.007 (e.g., 5,000,000 Yen → 35,000 USD)\n"
        "     • GBP: multiply by 1.30 (e.g., 10,000 GBP → 13,000 USD)\n"
        "     • AUD: multiply by 0.65 (e.g., 200,000 AUD → 130,000 USD)\n"
        "     • USD: use as-is\n"
        "   - Handle variations: '5k', '5 million', '$150k', '80,000'\n\n"
        "3. INDUSTRY CLASSIFICATION:\n"
        "   - Map business descriptions to Industry enum:\n"
        "     • Tech: software, AI, cloud, SaaS, startup, platform, DevOps, IoT, fintech app\n"
        "     • Finance: bank, investment, trading, insurance, fintech, credit union, payment processor\n"
        "     • Retail: bakery, shop, store, e-commerce, boutique, restaurant, wine shop, coffee shop\n"
        "     • Healthcare: hospital, clinic, pharma, medical, pharmaceutical, dental\n"
        "     • Other: if unclear or doesn't fit above\n\n"
        "4. SEGMENT INFERENCE:\n"
        "   - From contract value (if available):\n"
        "     • $100,000+ → Enterprise\n"
        "     • $25,000-$99,999 → Mid-Market\n"
        "     • <$25,000 → SMB\n"
        "   - From context: 'startup', 'small team', 'small practice' → SMB\n"
        "   - 'Fortune 500', 'enterprise software', 'multi-site' → Enterprise\n\n"
        "5. CONFIDENCE SCORING:\n"
        "   - Set confidence_score based on inference certainty:\n"
        "     • 1.0: All fields explicitly stated\n"
        "     • 0.8-0.9: Strong contextual evidence (city name + clear industry keywords)\n"
        "     • 0.6-0.7: Reasonable inference (some ambiguity)\n"
        "     • 0.4-0.5: Weak signals, uncertain\n\n"
        "6. DATA QUALITY RULES:\n"
        "   - Convert names to Title Case if needed\n"
        "   - Lowercase emails\n"
        "   - NEVER invent personal data (names, emails)\n"
        "   - If inference impossible, set field to None and lower confidence\n\n"
        "Return a fully valid SalesLead object with inferred fields populated from sales_notes."
    )
)


def repair_lead(invalid_row: dict, validation_error: str) -> SalesLead:
    """Attempt to repair an invalid lead using semantic inference.

    Args:
        invalid_row: Dictionary with incomplete/invalid data
        validation_error: Pydantic validation error message

    Returns:
        SalesLead with inferred fields populated

    Raises:
        Exception: If repair is impossible (e.g., missing critical data)
    """
    prompt = (
        f"Original data: {invalid_row}\n\n"
        f"Validation error: {validation_error}\n\n"
        "Please extract missing structured fields from the sales_notes. "
        "If sales_notes are provided, analyze them to infer country_code, "
        "industry, segment, and contract_value."
    )

    result = repair_agent.run_sync(prompt)
    return result.output
