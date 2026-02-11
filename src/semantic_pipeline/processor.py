"""Data processing pipeline with validation and AI repair."""

import csv
import json
import time
from pathlib import Path
from typing import Dict, List
from pydantic import ValidationError
from rich.console import Console

from .schemas import SalesLead
from .agent import repair_lead

console = Console()


class DataProcessor:
    """Process CSV data through validation and repair pipeline.

    The processor implements a 3-stage pipeline:
    1. Direct validation - Try to validate with strict Pydantic schema
    2. AI repair - Send invalid records to the AI agent for repair
    3. Failure logging - Track unrepairable records
    """

    def __init__(self, delay_between_repairs: float = 1.0, min_confidence: float = 0.0):
        """Initialize the data processor with empty result lists.

        Args:
            delay_between_repairs: Seconds to wait between repair attempts (default: 1.0)
            min_confidence: Minimum confidence score for repaired records (default: 0.0).
                Records below this threshold are stored in low_confidence_leads instead.
        """
        self.valid_leads: List[Dict] = []
        self.repaired_leads: List[Dict] = []
        self.failed_leads: List[Dict] = []
        self.low_confidence_leads: List[Dict] = []
        self.delay_between_repairs = delay_between_repairs
        self.min_confidence = min_confidence

    def process_csv(self, input_path: str) -> None:
        """Process CSV file through 3-stage pipeline.

        Args:
            input_path: Path to input CSV file
        """
        with open(input_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            # Convert string values to proper types
            try:
                typed_row = self._prepare_row(row)
            except Exception as e:
                self.failed_leads.append({
                    'row': row,
                    'stage': 'preprocessing',
                    'error': str(e)
                })
                continue

            # Pass 1: Direct validation
            try:
                lead = SalesLead.model_validate(typed_row)
                self.valid_leads.append(lead.model_dump())
                continue
            except ValidationError as e:
                validation_error = str(e)

            # Pass 2: AI repair attempt
            try:
                with console.status(f"[yellow]Repairing lead {row.get('id', '?')}...[/yellow]"):
                    repaired_lead = repair_lead(typed_row, validation_error)
                    repaired_data = repaired_lead.model_dump()
                    confidence = repaired_data.get('confidence_score', 0.0)

                    record = {
                        'original': row,
                        'repaired': repaired_data,
                        'error_fixed': validation_error
                    }

                    if confidence >= self.min_confidence:
                        self.repaired_leads.append(record)
                    else:
                        self.low_confidence_leads.append(record)

                    # Add delay after successful repair to avoid rate limits
                    time.sleep(self.delay_between_repairs)
            except Exception as repair_error:
                # Pass 3: Unrepairable
                self.failed_leads.append({
                    'row': row,
                    'stage': 'repair',
                    'validation_error': validation_error,
                    'repair_error': str(repair_error)
                })
                # Also add delay after failure to avoid rate limits
                time.sleep(self.delay_between_repairs)

    def _prepare_row(self, row: Dict[str, str]) -> Dict:
        """Convert CSV strings to proper types, handle optional fields.

        Args:
            row: Dictionary with string values from CSV

        Returns:
            Dictionary with properly typed values

        Raises:
            ValueError: If type conversion fails
        """
        # Start with required fields
        prepared = {
            'id': int(row['id']),
            'name': row['name'],
            'email': row['email'],
        }

        # Optional fields - only include if present and non-empty
        if row.get('country_code') and row['country_code'].strip():
            prepared['country_code'] = row['country_code']

        if row.get('industry') and row['industry'].strip():
            prepared['industry'] = row['industry']

        if row.get('segment') and row['segment'].strip():
            prepared['segment'] = row['segment']

        if row.get('contract_value') and row['contract_value'].strip():
            contract_value_str = row['contract_value'].replace('$', '').replace(',', '')
            prepared['contract_value'] = float(contract_value_str)

        if row.get('sales_notes') and row['sales_notes'].strip():
            prepared['sales_notes'] = row['sales_notes']

        if row.get('confidence_score') and row['confidence_score'].strip():
            prepared['confidence_score'] = float(row['confidence_score'])

        return prepared

    def save_results(self, output_dir: str = 'outputs') -> None:
        """Save results to JSON files.

        Creates three output files:
        - valid.json: Records that passed strict validation
        - repaired.json: Records fixed by the AI agent
        - failed.json: Unrepairable records

        Args:
            output_dir: Directory to save output files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        with open(output_path / 'valid.json', 'w') as f:
            json.dump(self.valid_leads, f, indent=2)

        with open(output_path / 'repaired.json', 'w') as f:
            json.dump(self.repaired_leads, f, indent=2)

        with open(output_path / 'failed.json', 'w') as f:
            json.dump(self.failed_leads, f, indent=2)

        if self.low_confidence_leads:
            with open(output_path / 'low_confidence.json', 'w') as f:
                json.dump(self.low_confidence_leads, f, indent=2)
