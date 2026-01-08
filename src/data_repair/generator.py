"""Generate sample sales lead data for testing."""

import csv
import random
from pathlib import Path


def generate_sample_data(output_path: str) -> None:
    """Generate 50 sample sales leads with varying quality.

    Distribution:
    - 30 clean records: Perfect data that passes validation
    - 15 fixable records: Data with issues the AI can repair
    - 5 unfixable records: Data that cannot be repaired

    Args:
        output_path: Path to output CSV file
    """
    leads = []

    # 30 CLEAN RECORDS - Perfect validation
    clean_names = [
        "Alice Johnson", "Bob Smith", "Carol Davis", "David Brown",
        "Emma Wilson", "Frank Miller", "Grace Lee", "Henry Taylor"
    ]
    clean_countries = ["US", "GB", "DE", "FR", "JP", "AU", "CA", "ES"]

    for i in range(1, 31):
        leads.append({
            'id': i,
            'name': random.choice(clean_names),
            'email': f"user{i}@company.com",
            'country_code': random.choice(clean_countries),
            'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
            'contract_value': f"{random.randint(10000, 200000)}.00"
        })

    # 15 FIXABLE RECORDS - AI should repair these
    fixable_data = [
        # Country name variations (non-ISO codes)
        {'id': 31, 'name': 'John Doe', 'email': 'john@example.com',
         'country_code': 'USA', 'segment': 'Enterprise', 'contract_value': '50000'},
        {'id': 32, 'name': 'Jane Smith', 'email': 'jane@example.com',
         'country_code': 'usa', 'segment': 'Mid-Market', 'contract_value': '30000'},
        {'id': 33, 'name': 'Mike Johnson', 'email': 'mike@test.com',
         'country_code': 'United States', 'segment': 'SMB', 'contract_value': '15000'},
        {'id': 34, 'name': 'Sarah Wilson', 'email': 'sarah@test.com',
         'country_code': 'UK', 'segment': 'Enterprise', 'contract_value': '120000'},
        {'id': 35, 'name': 'Tom Brown', 'email': 'tom@example.com',
         'country_code': 'germany', 'segment': 'Mid-Market', 'contract_value': '45000'},

        # Name case issues (not Title Case)
        {'id': 36, 'name': 'alice cooper', 'email': 'alice@example.com',
         'country_code': 'US', 'segment': 'SMB', 'contract_value': '12000'},
        {'id': 37, 'name': 'BOB MARLEY', 'email': 'bob@music.com',
         'country_code': 'GB', 'segment': 'Enterprise', 'contract_value': '95000'},
        {'id': 38, 'name': 'charlie chaplin', 'email': 'charlie@film.com',
         'country_code': 'FR', 'segment': 'Mid-Market', 'contract_value': '38000'},

        # Segment variations (not exact enum values)
        {'id': 39, 'name': 'Diana Prince', 'email': 'diana@corp.com',
         'country_code': 'US', 'segment': 'small business', 'contract_value': '8000'},
        {'id': 40, 'name': 'Eric Cartman', 'email': 'eric@southpark.com',
         'country_code': 'US', 'segment': 'enterprise', 'contract_value': '150000'},

        # Contract value formatting issues
        {'id': 41, 'name': 'Fiona Apple', 'email': 'fiona@music.com',
         'country_code': 'US', 'segment': 'Mid-Market', 'contract_value': '$45,000'},
        {'id': 42, 'name': 'George Lucas', 'email': 'george@starwars.com',
         'country_code': 'US', 'segment': 'Enterprise', 'contract_value': '$200,000.00'},

        # Multiple issues combined
        {'id': 43, 'name': 'helen mirren', 'email': 'HELEN@EXAMPLE.COM',
         'country_code': 'uk', 'segment': 'enterprise', 'contract_value': '$105,000'},
        {'id': 44, 'name': 'IVAN DRAGO', 'email': 'ivan@boxing.ru',
         'country_code': 'russia', 'segment': 'mid-market', 'contract_value': '52000'},
        {'id': 45, 'name': 'julia roberts', 'email': 'julia@hollywood.com',
         'country_code': 'USA', 'segment': 'Enterprise', 'contract_value': '$88,500'},
    ]
    leads.extend(fixable_data)

    # 5 UNFIXABLE RECORDS - Should fail completely
    unfixable_data = [
        {'id': 46, 'name': '', 'email': 'noempty@test.com',
         'country_code': 'US', 'segment': 'Enterprise', 'contract_value': '50000'},
        {'id': 47, 'name': 'Invalid Email', 'email': 'not-an-email',
         'country_code': 'US', 'segment': 'SMB', 'contract_value': '10000'},
        {'id': 48, 'name': 'Negative Value', 'email': 'negative@test.com',
         'country_code': 'US', 'segment': 'Mid-Market', 'contract_value': '-5000'},
        {'id': 49, 'name': 'Bad Country', 'email': 'bad@test.com',
         'country_code': 'ZZZ', 'segment': 'Enterprise', 'contract_value': '75000'},
        {'id': 50, 'name': 'Missing Data', 'email': '',
         'country_code': '', 'segment': '', 'contract_value': '0'},
    ]
    leads.extend(unfixable_data)

    # Write to CSV
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'name', 'email', 'country_code', 'segment', 'contract_value'
        ])
        writer.writeheader()
        writer.writerows(leads)
