"""Generate sample sales lead data with semantic extraction challenges."""

import csv
import random
from pathlib import Path


def generate_sample_data(output_path: str, size: int = 50) -> None:
    """Generate sample sales leads with varying quality levels.

    Distribution (scalable based on size):
    - 40% clean records: Perfect data with all fields filled
    - 50% incomplete records: Missing fields with rich sales_notes for semantic extraction
    - 10% unfixable records: Invalid data that can't be inferred

    Args:
        output_path: Path to output CSV file
        size: Number of records to generate (default: 50)
    """
    leads = []

    # Calculate distribution
    clean_count = int(size * 0.40)
    incomplete_count = int(size * 0.50)
    unfixable_count = size - clean_count - incomplete_count

    # 40% PERFECT RECORDS - All fields complete
    clean_names = [
        "Alice Johnson", "Bob Smith", "Carol Davis", "David Brown",
        "Emma Wilson", "Frank Miller", "Grace Lee", "Henry Taylor"
    ]
    clean_countries = ["US", "GB", "DE", "FR", "JP", "AU", "CA", "ES"]
    clean_industries = ["Tech", "Finance", "Retail", "Healthcare"]

    for i in range(1, clean_count + 1):
        leads.append({
            'id': i,
            'name': random.choice(clean_names),
            'email': f"user{i}@company.com",
            'country_code': random.choice(clean_countries),
            'industry': random.choice(clean_industries),
            'segment': random.choice(['Enterprise', 'Mid-Market', 'SMB']),
            'contract_value': f"{random.randint(10000, 200000)}.00",
            'sales_notes': '',
            'confidence_score': '1.0'
        })

    # 50% INCOMPLETE RECORDS - Need semantic extraction from sales_notes
    incomplete_data = [
        # Geography + Retail + EUR conversion
        {
            'id': clean_count + 1, 'name': 'Sophie Martin', 'email': 'sophie.martin@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Lunch meeting in Paris with small bakery owner. Budget around 5000 EUR for POS system.',
            'confidence_score': '0.0'
        },
        # Geography + Finance + JPY conversion
        {
            'id': clean_count + 2, 'name': 'Yuki Tanaka', 'email': 'yuki.tanaka@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Meeting in Tokyo with Mizuho Bank executive. Enterprise software project: 5 million Yen budget.',
            'confidence_score': '0.0'
        },
        # Geography + Tech + USD
        {
            'id': clean_count + 3, 'name': 'Michael Chen', 'email': 'michael.chen@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Call with CTO of Silicon Valley AI startup. Series A funded. Cloud platform spend: $150k.',
            'confidence_score': '0.0'
        },
        # Geography + Healthcare + GBP conversion
        {
            'id': clean_count + 4, 'name': 'Oliver Clarke', 'email': 'oliver.clarke@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'London hospital administrator interested in medical records system. Budget: 80,000 GBP.',
            'confidence_score': '0.0'
        },
        # Geography + Retail + segment inference
        {
            'id': clean_count + 5, 'name': 'Emma Schmidt', 'email': 'emma.schmidt@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Berlin boutique owner. Small fashion e-commerce platform needed. Budget: 15k EUR.',
            'confidence_score': '0.0'
        },
        # Tech + Various locations
        {
            'id': clean_count + 6, 'name': 'James Anderson', 'email': 'james.anderson@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Toronto-based SaaS company building HR platform. Looking at $75k annual contract.',
            'confidence_score': '0.0'
        },
        # Finance + Currency
        {
            'id': clean_count + 7, 'name': 'Maria Garcia', 'email': 'maria.garcia@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Insurance firm in Sydney discussing claims processing system. Budget 200,000 AUD.',
            'confidence_score': '0.0'
        },
        # Healthcare + implicit location
        {
            'id': clean_count + 8, 'name': 'Thomas Mueller', 'email': 'thomas.mueller@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'German hospital network needs patient management software. 120k EUR available.',
            'confidence_score': '0.0'
        },
        # Retail + USD
        {
            'id': clean_count + 9, 'name': 'Lisa Wang', 'email': 'lisa.wang@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'E-commerce store in New York. Small team needs inventory system for $18k.',
            'confidence_score': '0.0'
        },
        # Tech + JPY
        {
            'id': clean_count + 10, 'name': 'Kenji Yamamoto', 'email': 'kenji.yamamoto@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Meeting with Tokyo startup. Developing fintech app. Seed funded: 8 million Yen budget.',
            'confidence_score': '0.0'
        },
        # Finance + GBP
        {
            'id': clean_count + 11, 'name': 'Charlotte Brown', 'email': 'charlotte.brown@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Investment bank in the City of London. Trading platform upgrade: 250k GBP.',
            'confidence_score': '0.0'
        },
        # Healthcare + EUR
        {
            'id': clean_count + 12, 'name': 'Pierre Dubois', 'email': 'pierre.dubois@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Paris clinic looking for telemedicine solution. Small practice, 8000 EUR budget.',
            'confidence_score': '0.0'
        },
        # Tech + Enterprise context
        {
            'id': clean_count + 13, 'name': 'Sarah Williams', 'email': 'sarah.williams@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Fortune 500 company in Seattle. Enterprise cloud migration project: $500k.',
            'confidence_score': '0.0'
        },
        # Retail + Ambiguous
        {
            'id': clean_count + 14, 'name': 'Carlos Rodriguez', 'email': 'carlos.rodriguez@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Restaurant chain needs POS system. Based in Madrid. 35k EUR.',
            'confidence_score': '0.0'
        },
        # Finance + Context clue
        {
            'id': clean_count + 15, 'name': 'Anna Kowalski', 'email': 'anna.kowalski@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Credit union in Warsaw exploring core banking upgrade. 180k USD equivalent.',
            'confidence_score': '0.0'
        },
        # Tech + Startup context
        {
            'id': clean_count + 16, 'name': 'David Kim', 'email': 'david.kim@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Seoul-based gaming startup. 12 employees. Looking at analytics platform: $40k.',
            'confidence_score': '0.0'
        },
        # Healthcare + Large scale
        {
            'id': clean_count + 17, 'name': 'Jennifer Lee', 'email': 'jennifer.lee@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Hospital network across Australia. Multi-site EHR system. $2M AUD total.',
            'confidence_score': '0.0'
        },
        # Retail + Small
        {
            'id': clean_count + 18, 'name': 'Giovanni Rossi', 'email': 'giovanni.rossi@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Family-owned wine shop in Milan. Simple e-commerce site needed: 6k EUR.',
            'confidence_score': '0.0'
        },
        # Finance + Mid-market
        {
            'id': clean_count + 19, 'name': 'Emma Thompson', 'email': 'emma.thompson@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'UK-based wealth management firm. 50 advisors. CRM system: 85k GBP.',
            'confidence_score': '0.0'
        },
        # Tech + Ambiguous location
        {
            'id': clean_count + 20, 'name': 'Hassan Ahmed', 'email': 'hassan.ahmed@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Software company building DevOps tools. Remote team. Looking for CI/CD: $95k.',
            'confidence_score': '0.0'
        },
        # Healthcare + Pharma
        {
            'id': clean_count + 21, 'name': 'Isabella Martinez', 'email': 'isabella.martinez@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Pharmaceutical lab in Barcelona. Clinical trial management system: 140k EUR.',
            'confidence_score': '0.0'
        },
        # Retail + Chain
        {
            'id': clean_count + 22, 'name': 'Ryan O\'Connor', 'email': 'ryan.oconnor@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Irish coffee shop chain (8 locations). Loyalty app development: 28k EUR.',
            'confidence_score': '0.0'
        },
        # Finance + Fintech
        {
            'id': clean_count + 23, 'name': 'Alexandra Petrov', 'email': 'alexandra.petrov@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Payment processor startup. San Francisco based. Series B. Infrastructure: $320k.',
            'confidence_score': '0.0'
        },
        # Tech + Cloud
        {
            'id': clean_count + 24, 'name': 'Mohammed Al-Farsi', 'email': 'mohammed.alfarsi@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Dubai tech firm building IoT platform. Cloud infrastructure budget: $180k USD.',
            'confidence_score': '0.0'
        },
        # Healthcare + Small clinic
        {
            'id': clean_count + 25, 'name': 'Sophie Laurent', 'email': 'sophie.laurent@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Dental practice in Brussels. 3 dentists. Appointment scheduling system: 9k EUR.',
            'confidence_score': '0.0'
        },
    ]

    # Take only what we need for the distribution
    leads.extend(incomplete_data[:incomplete_count])

    # 10% UNFIXABLE RECORDS - Invalid data that can't be inferred
    start_id = clean_count + incomplete_count + 1
    unfixable_data = [
        # Empty name (critical field missing)
        {
            'id': start_id, 'name': '', 'email': 'noempty@test.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Some vague notes without useful context.',
            'confidence_score': '0.0'
        },
        # Invalid email (can't be fixed)
        {
            'id': start_id + 1, 'name': 'Invalid Email Person', 'email': 'not-an-email',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Interested in software but no clear details.',
            'confidence_score': '0.0'
        },
        # No useful context in notes
        {
            'id': start_id + 2, 'name': 'John Mystery', 'email': 'john.mystery@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Follow up next week.',
            'confidence_score': '0.0'
        },
        # Ambiguous/contradictory information
        {
            'id': start_id + 3, 'name': 'Jane Unclear', 'email': 'jane.unclear@example.com',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Works for a company. Maybe interested in something. Budget unclear.',
            'confidence_score': '0.0'
        },
        # Missing critical email field
        {
            'id': start_id + 4, 'name': 'Missing Email', 'email': '',
            'country_code': '', 'industry': '', 'segment': '', 'contract_value': '',
            'sales_notes': 'Technology firm in London looking at CRM. 50k GBP budget.',
            'confidence_score': '0.0'
        },
    ]

    leads.extend(unfixable_data[:unfixable_count])

    # Write to CSV
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'name', 'email', 'country_code', 'industry', 'segment',
            'contract_value', 'sales_notes', 'confidence_score'
        ])
        writer.writeheader()
        writer.writerows(leads)
