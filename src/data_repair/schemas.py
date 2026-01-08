"""Pydantic models for strict data validation."""

from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class Segment(str, Enum):
    """Customer segment categories."""
    ENTERPRISE = "Enterprise"
    MID_MARKET = "Mid-Market"
    SMB = "SMB"


class SalesLead(BaseModel):
    """Strict sales lead schema with comprehensive validation.

    This model enforces strict typing and validation rules to ensure
    100% schema compliance for sales lead data.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False
    )

    id: int = Field(ge=1, description="Unique lead identifier")

    name: str = Field(
        min_length=2,
        description="Lead name in Title Case"
    )

    email: EmailStr = Field(
        description="Valid email address"
    )

    country_code: str = Field(
        pattern="^[A-Z]{2}$",
        description="ISO 3166-1 alpha-2 country code (e.g., US, JP, DE)"
    )

    segment: Segment = Field(
        description="Customer segment classification"
    )

    contract_value: float = Field(
        gt=0.0,
        description="Positive contract value in USD"
    )

    @field_validator('name')
    @classmethod
    def validate_title_case(cls, v: str) -> str:
        """Ensure name is in Title Case.

        Args:
            v: Name string to validate

        Returns:
            Validated name string

        Raises:
            ValueError: If name is not in Title Case
        """
        if not v.istitle():
            raise ValueError(f"Name must be in Title Case, got: {v}")
        return v
