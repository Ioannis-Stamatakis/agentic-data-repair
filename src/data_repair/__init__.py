"""Agentic Data Repair - AI-powered data quality pipeline.

A self-healing data pipeline that uses Pydantic AI and Google Gemini
to automatically repair invalid data records, ensuring 100% schema compliance.
"""

__version__ = "1.0.0"
__author__ = "Agentic Data Repair Contributors"
__license__ = "MIT"

from .schemas import SalesLead, Segment
from .agent import repair_agent, repair_lead
from .processor import DataProcessor

__all__ = [
    "SalesLead",
    "Segment",
    "repair_agent",
    "repair_lead",
    "DataProcessor",
]
