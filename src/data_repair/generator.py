"""Generate sample sales lead data for testing."""

import csv
import random
from pathlib import Path


def generate_sample_data(output_path: str, size: int = 50) -> None:
    """Generate sample sales leads with varying quality.

    Distribution (scalable based on size):
    - 60% clean records: Perfect data that passes validation
    - 30% fixable records: Data with issues the AI can repair
    - 10% unfixable records: Data that cannot be repaired

    Args:
        output_path: Path to output CSV file
        size: Total number of records to generate (default: 50)
    """
    leads = []

    # Calculate distribution
    clean_count = int(size * 0.60)
    fixable_count = int(size * 0.30)
    unfixable_count = size - clean_count - fixable_count

    # Name pools
    clean_names = [
        "Alice Johnson", "Bob Smith", "Carol Davis", "David Brown",
        "Emma Wilson", "Frank Miller", "Grace Lee", "Henry Taylor",
        "Isabel Martinez", "James Wilson", "Katherine White", "Lucas Brown",
        "Maria Garcia", "Nathan Lee", "Olivia Anderson", "Patrick Clark"
    ]

    dirty_names = [
        "alice cooper", "BOB MARLEY", "charlie chaplin", "DIANA ROSS",
        "eddie murphy", "FRANK SINATRA", "grace jones", "HARRY STYLES",
        "isaac newton", "JANE AUSTEN", "kevin hart", "LISA SIMPSON",
        "michael jordan", "NANCY DREW", "oscar wilde", "PAULA ABDUL"
    ]

    clean_countries = ["US", "GB", "DE", "FR", "JP", "AU", "CA", "ES"]

    # Country variations for AI to fix
    dirty_countries = [
        "USA", "usa", "United States", "America", "U.S.", "U.S.A.",
        "UK", "uk", "United Kingdom", "Britain", "England",
        "germany", "Deutschland", "GERMANY",
        "france", "FRANCE", "Francia",
        "japan", "JAPAN", "Nippon",
        "australia", "AUSTRALIA", "Aus",
        "canada", "CANADA", "CAN",
        "spain", "SPAIN", "España", "spain",
        "italy", "ITALY", "IT", "Italia",
        "russia", "RUSSIA", "RU"
    ]

    # Segment variations
    segment_variations = {
        'Enterprise': ['enterprise', 'ENTERPRISE', 'large', 'big business', 'corporate'],
        'Mid-Market': ['mid-market', 'MID-MARKET', 'midmarket', 'medium', 'mid market'],
        'SMB': ['smb', 'SMB', 'small business', 'small', 'startup', 'small-medium']
    }

    email_domains = ['company.com', 'example.com', 'business.org', 'corp.io', 'test.com', 'acme.com']

    current_id = 1

    # CLEAN RECORDS - Perfect validation
    for i in range(clean_count):
        leads.append({
            'id': current_id,
            'name': random.choice(clean_names),
            'email': f"user{current_id}@{random.choice(email_domains)}",
            'country_code': random.choice(clean_countries),
            'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
            'contract_value': f"{random.randint(10000, 200000)}.00"
        })
        current_id += 1

    # FIXABLE RECORDS - AI should repair these (30% of total)
    for i in range(fixable_count):
        issue_type = random.choice(['country', 'name', 'segment', 'value', 'multiple'])
        correct_segment = random.choice(['Enterprise', 'Mid-Market', 'SMB'])
        contract_val = random.randint(10000, 200000)

        if issue_type == 'country':
            # Just country code issue
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(dirty_countries),
                'segment': correct_segment,
                'contract_value': str(contract_val)
            })
        elif issue_type == 'name':
            # Just name casing issue
            leads.append({
                'id': current_id,
                'name': random.choice(dirty_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(clean_countries),
                'segment': correct_segment,
                'contract_value': str(contract_val)
            })
        elif issue_type == 'segment':
            # Just segment variation
            segment_vars = random.choice(list(segment_variations.values()))
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(clean_countries),
                'segment': random.choice(segment_vars),
                'contract_value': str(contract_val)
            })
        elif issue_type == 'value':
            # Just value formatting issue
            formatted_val = random.choice([
                f"${contract_val:,}",
                f"${contract_val:,.2f}",
                f"${contract_val}",
                f"{contract_val:,}"
            ])
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(clean_countries),
                'segment': correct_segment,
                'contract_value': formatted_val
            })
        else:  # multiple issues
            # Combine 2-3 issues
            segment_vars = random.choice(list(segment_variations.values()))
            formatted_val = random.choice([
                f"${contract_val:,}",
                f"${contract_val:,.2f}",
            ])
            email = f"user{current_id}@{random.choice(email_domains)}"
            if random.random() > 0.5:
                email = email.upper()  # Uppercase email

            leads.append({
                'id': current_id,
                'name': random.choice(dirty_names),
                'email': email,
                'country_code': random.choice(dirty_countries),
                'segment': random.choice(segment_vars),
                'contract_value': formatted_val
            })

        current_id += 1

    # UNFIXABLE RECORDS - Should fail completely (10% of total)
    unfixable_types = ['empty_name', 'invalid_email', 'negative_value', 'bad_country', 'zero_value']

    for i in range(unfixable_count):
        issue = unfixable_types[i % len(unfixable_types)]

        if issue == 'empty_name':
            leads.append({
                'id': current_id,
                'name': '',
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(clean_countries),
                'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
                'contract_value': str(random.randint(10000, 100000))
            })
        elif issue == 'invalid_email':
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': random.choice(['not-an-email', 'missing@', '@nodomain.com', 'no-at-sign.com']),
                'country_code': random.choice(clean_countries),
                'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
                'contract_value': str(random.randint(10000, 100000))
            })
        elif issue == 'negative_value':
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(clean_countries),
                'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
                'contract_value': str(random.randint(-50000, -1000))
            })
        elif issue == 'bad_country':
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names),
                'email': f"user{current_id}@{random.choice(email_domains)}",
                'country_code': random.choice(['ZZZ', 'XXX', 'QQQ', '123', 'INVALID']),
                'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
                'contract_value': str(random.randint(10000, 100000))
            })
        else:  # zero_value
            leads.append({
                'id': current_id,
                'name': random.choice(clean_names) if random.random() > 0.5 else '',
                'email': f"user{current_id}@{random.choice(email_domains)}" if random.random() > 0.5 else '',
                'country_code': random.choice(clean_countries) if random.random() > 0.5 else '',
                'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']) if random.random() > 0.5 else '',
                'contract_value': '0'
            })

        current_id += 1

    # Write to CSV
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'name', 'email', 'country_code', 'segment', 'contract_value'
        ])
        writer.writeheader()
        writer.writerows(leads)
