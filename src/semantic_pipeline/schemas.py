"""Pydantic models for strict data validation."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class Segment(str, Enum):
    """Customer segment categories."""
    ENTERPRISE = "Enterprise"
    MID_MARKET = "Mid-Market"
    SMB = "SMB"


class Industry(str, Enum):
    """Industry classifications."""
    TECH = "Tech"
    FINANCE = "Finance"
    RETAIL = "Retail"
    HEALTHCARE = "Healthcare"
    OTHER = "Other"


class SalesLead(BaseModel):
    """Sales lead schema with semantic inference support.

    This model supports both complete records and incomplete records that require
    semantic extraction from unstructured sales_notes field.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False
    )

    # Required fields (always present)
    id: int = Field(ge=1, description="Unique lead identifier")

    name: str = Field(
        min_length=2,
        description="Lead name in Title Case"
    )

    email: EmailStr = Field(
        description="Valid email address"
    )

    # Optional fields (can be inferred from sales_notes)
    country_code: Optional[str] = Field(
        default=None,
        pattern="^[A-Z]{2}$",
        description="ISO 3166-1 alpha-2 country code (e.g., US, JP, DE)"
    )

    industry: Optional[Industry] = Field(
        default=None,
        description="Industry classification"
    )

    segment: Optional[Segment] = Field(
        default=None,
        description="Customer segment classification"
    )

    contract_value: Optional[float] = Field(
        default=None,
        gt=0.0,
        description="Positive contract value in USD"
    )

    # New fields for semantic inference
    sales_notes: Optional[str] = Field(
        default=None,
        description="Unstructured notes containing context for missing fields"
    )

    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for inferred fields (0.0-1.0)"
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

    def model_post_init(self, __context) -> None:
        """Validate that records with sales_notes have extracted fields.

        If sales_notes is present but key fields are missing, this should
        trigger AI extraction, not pass validation.
        """
        if self.sales_notes and self.sales_notes.strip():
            # If we have sales notes but missing critical fields, fail validation
            if not self.country_code or not self.industry or not self.contract_value:
                raise ValueError(
                    "Record has sales_notes but missing extracted fields. "
                    "This indicates semantic extraction is needed."
                )
