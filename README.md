# 🤖 Semantic Data Pipeline Agent

> AI-powered semantic extraction pipeline - transforms unstructured text into structured data using Pydantic AI & Google Gemini

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-0.0.15+-green.svg)](https://ai.pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Why This Project?

**Traditional validators reject bad data. This tool extracts meaning from it.**

Most data pipelines fail when encountering incomplete records. This CLI tool uses an **AI agent** to perform **semantic extraction** - extracting structured fields (country codes, industries, contract values) from unstructured natural language text.

Perfect for:
- 🏢 Sales lead enrichment from CRM notes
- 🌐 Geographic entity extraction
- 💰 Multi-currency data normalization
- 🔧 Unstructured data transformation

---

## ✨ Features

- **Semantic Extraction** - AI extracts structured data from unstructured text
- **Geographic Intelligence** - Maps cities to ISO country codes (Paris→FR, Tokyo→JP)
- **Currency Conversion** - Handles EUR, GBP, JPY, AUD with automatic USD conversion
- **Industry Classification** - Categorizes businesses from descriptions
- **Type-Safe AI** - Pydantic AI ensures structured outputs with full validation
- **Beautiful Terminal UI** - Rich tables showing extraction results with confidence scores
- **Rate Limit Protection** - Exponential backoff + inter-row delays handle API limits

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/semantic-data-pipeline-agent.git
cd semantic-data-pipeline-agent

# Install with pip
pip install -e .

# Set up API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Usage

```bash
# Generate sample dataset with semantic extraction challenges
pipeline generate --size 30

# Run the semantic extraction pipeline
pipeline clean examples/sample_leads.csv

# View results
cat outputs/valid.json      # Records passing validation
cat outputs/repaired.json   # AI-extracted records
cat outputs/failed.json     # Unrepairable records
```

---

## 📊 Example Output

```
╭────────────────────────────────────────────╮
│  Semantic Data Pipeline Agent             │
│  AI-Powered Semantic Extraction           │
╰────────────────────────────────────────────╯

Processing: examples/sample_leads.csv
Mode: Semantic Extraction Pipeline (Validate → Extract → Report)

                          PIPELINE RESULTS
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Category             ┃      Count ┃   Percentage ┃ Status                   ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✓ Valid              │         12 │        40.0% │ Passed strict validation │
│ ⚙ Repaired by AI     │          6 │        20.0% │ Semantic extraction      │
│ ✗ Failed             │         12 │        40.0% │ Unrepairable records     │
│ TOTAL PROCESSED      │         30 │       100.0% │                          │
└──────────────────────┴────────────┴──────────────┴──────────────────────────┘

                          SEMANTIC EXTRACTION EXAMPLES
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID  ┃ Input Note                                                    ┃ Country  ┃ Industry   ┃ Value (USD)  ┃ Confidence ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 16  │ London hospital administrator interested in medical records   │ GB       │ Healthcare │ $104,000     │ 90.0%      │
│     │ system. Budget: 80,000 GBP.                                   │          │            │              │            │
│ 17  │ Berlin boutique owner. Small fashion e-commerce platform      │ DE       │ Retail     │ $16,500      │ 90.0%      │
│     │ needed. Budget: 15k EUR.                                      │          │            │              │            │
│ 21  │ E-commerce store in New York. Small team needs inventory      │ US       │ Retail     │ $18,000      │ 90.0%      │
│     │ system for $18k.                                              │          │            │              │            │
│ 22  │ Meeting with Tokyo startup. Developing fintech app. Seed      │ JP       │ Finance    │ $56,000      │ 90.0%      │
│     │ funded: 8 million Yen budget.                                 │          │            │              │            │
│ 23  │ Investment bank in the City of London. Trading platform       │ GB       │ Finance    │ $325,000     │ 90.0%      │
│     │ upgrade: 250k GBP.                                            │          │            │              │            │
└─────┴───────────────────────────────────────────────────────────────┴──────────┴────────────┴──────────────┴────────────┘
```

---

## 🏗️ Architecture

### Pipeline Flow

```
CSV Input → Strict Validation → Semantic Extraction → Structured Output
              ↓ Pass                  ↓ Pass               ↓
           valid.json            repaired.json       failed.json
```

### Tech Stack

- **Pydantic AI** - Type-safe LLM agents with structured outputs
- **Google Gemini 2.5 Flash Lite** - Fast, cost-effective semantic extraction
- **Pydantic V2** - Runtime validation with optional fields
- **Typer + Rich** - Professional CLI with beautiful terminal UI

---

## 🧠 Semantic Extraction Capabilities

### 1. Geographic Extraction
Maps city names and contextual clues to ISO 3166-1 alpha-2 country codes:
- **Cities:** Paris→FR, Tokyo→JP, London→GB, Berlin→DE, New York→US
- **Context:** "Silicon Valley"→US, "City of London"→GB, "Mizuho Bank"→JP

### 2. Currency Conversion
Detects foreign currencies and converts to USD:
- **EUR:** ×1.10 (5000 EUR → $5,500)
- **GBP:** ×1.30 (80,000 GBP → $104,000)
- **JPY:** ×0.007 (8M Yen → $56,000)
- **AUD:** ×0.65 (200k AUD → $130,000)
- Handles variations: "5k", "$150k", "5 million"

### 3. Industry Classification
Categorizes businesses from keywords into structured enums:
- **Tech:** software, AI, cloud, SaaS, startup, platform
- **Finance:** bank, investment, trading, insurance, fintech
- **Retail:** bakery, shop, store, e-commerce, boutique
- **Healthcare:** hospital, clinic, pharma, medical

### 4. Segment Inference
Determines customer segment from context:
- **Enterprise:** $100k+ contracts, "Fortune 500", "multi-site"
- **Mid-Market:** $25k-$99k contracts
- **SMB:** <$25k contracts, "startup", "small team"

### 5. Confidence Scoring
AI assigns confidence scores (0.0-1.0) based on inference certainty:
- **1.0:** All fields explicitly stated
- **0.8-0.9:** Strong contextual evidence
- **0.6-0.7:** Reasonable inference
- **0.4-0.5:** Weak signals, uncertain

---

## 🔍 Why Pydantic AI?

Unlike raw LLM APIs, Pydantic AI enforces **type safety on AI outputs**:

```python
# Without Pydantic AI - hope the LLM returns valid JSON
response = llm.generate("Extract data: ...")
data = json.loads(response)  # ❌ Might crash

# With Pydantic AI - guaranteed type safety
result = agent.run_sync("Extract data: ...")
lead: SalesLead = result.output  # ✅ Type-safe, validated
```

The agent MUST return a valid `SalesLead` object or raise an error. No surprises.

---

## 📝 Schema Example

```python
class Industry(str, Enum):
    TECH = "Tech"
    FINANCE = "Finance"
    RETAIL = "Retail"
    HEALTHCARE = "Healthcare"
    OTHER = "Other"

class SalesLead(BaseModel):
    # Required fields
    id: int                              # Positive integer
    name: str                            # Title Case validated
    email: EmailStr                      # RFC 5322 compliant

    # Optional (can be inferred from sales_notes)
    country_code: Optional[str]          # ISO alpha-2 (^[A-Z]{2}$)
    industry: Optional[Industry]         # Enum
    segment: Optional[Segment]           # Enum
    contract_value: Optional[float]      # Positive USD amount

    # Semantic inference fields
    sales_notes: Optional[str]           # Unstructured input
    confidence_score: float = 1.0        # 0.0-1.0
```

**Key Feature:** If `sales_notes` is present but fields are missing, triggers AI semantic extraction (enforced by `model_post_init` validator).

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Semantic NLP** - Entity extraction, currency conversion, contextual reasoning
2. **Modern Python** - 3.11+, type hints, pyproject.toml
3. **Pydantic AI agents** - Type-safe structured outputs
4. **Data validation** - Optional fields, custom validators
5. **Production patterns** - Rate limiting, exponential backoff, error handling
6. **Professional CLI** - Typer + Rich with beautiful UX

---

## 🛠️ Project Structure

```
semantic-data-pipeline-agent/
├── src/
│   └── semantic_pipeline/
│       ├── __init__.py        # Package initialization
│       ├── schemas.py         # Pydantic models with Industry enum
│       ├── agent.py           # Gemini agent with retry logic
│       ├── processor.py       # Pipeline with rate limiting
│       ├── generator.py       # Sample data generator
│       └── cli.py             # CLI commands
├── examples/
│   └── sample_leads.csv       # Generated test data
├── outputs/                   # Pipeline results
│   ├── valid.json
│   ├── repaired.json
│   └── failed.json
├── pyproject.toml             # Modern Python packaging
├── README.md
├── CLAUDE.md                  # Developer guide
├── LICENSE
└── .env.example
```

---

## 📈 Sample Data Distribution

The generated dataset includes:

**40% Valid Records** - Complete data passing validation:
- All fields populated with valid values
- No semantic extraction needed

**50% Incomplete Records** - Requires semantic extraction:
- Missing fields but rich `sales_notes` with context
- Examples: "Meeting in Paris with bakery owner. Budget: 5000 EUR"
- AI extracts: FR, Retail, $5,500, 0.9 confidence

**10% Unfixable Records** - Cannot be repaired:
- Empty names or invalid emails
- Vague notes without useful context
- Truly incomplete data

---

## 🔧 Advanced Features

### Rate Limiting Protection

**Two-layer strategy to handle API limits:**

1. **Exponential Backoff** (agent.py)
   - Max 3 retries per record
   - Wait times: 2s → 4s → 8s
   - Only retries on 503/overloaded errors

2. **Inter-Row Delay** (processor.py)
   - 1.0s delay between each extraction
   - Prevents rapid-fire API requests
   - Configurable via `DataProcessor(delay_between_repairs=X)`

**Trade-off:** Slower processing (up to 15s per problematic record) vs higher success rate

---

## 🤝 Contributing

Contributions welcome! This is a portfolio project demonstrating modern Python and AI best practices.

Areas for improvement:
- Async processing with `agent.run()` for large datasets
- Unit tests with pytest + mock API
- Expose `delay_between_repairs` as CLI option
- Support more country variations (full names)
- Repair statistics dashboard

---

## 📄 License

MIT © 2026 Semantic Data Pipeline Agent Contributors

See [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Pydantic AI Documentation**: https://ai.pydantic.dev/
- **Google Gemini API**: https://ai.google.dev/
- **Pydantic V2**: https://docs.pydantic.dev/
- **Typer**: https://typer.tiangolo.com/
- **Rich**: https://rich.readthedocs.io/

---

## 🙏 Acknowledgments

Built with:
- [Pydantic AI](https://ai.pydantic.dev/) - Type-safe AI agents
- [Google Gemini](https://ai.google.dev/) - Semantic extraction model
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

**Made with ❤️ for the AI & data engineering community**
