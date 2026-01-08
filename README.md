# 🤖 Agentic Data Repair

> A self-healing data pipeline powered by Pydantic AI & Google Gemini

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-0.0.15+-green.svg)](https://ai.pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Why This Project?

**Traditional validators reject bad data. This tool *fixes* it.**

Most data pipelines fail when encountering invalid records. This CLI tool uses an **AI agent** to understand validation errors and intelligently repair data, ensuring 100% schema compliance.

Perfect for:
- 🏢 Sales lead normalization
- 🌐 International data cleanup
- 📊 ETL pipeline resilience
- 🔧 Legacy data migration

---

## ✨ Features

- **Strict Pydantic V2 Validation** - Zero tolerance for bad data
- **AI-Powered Repair** - Gemini 2.5 Flash understands and fixes errors
- **Intelligent Normalization**:
  - Country names → ISO codes ("United States" → "US")
  - Name formatting → Title Case ("john smith" → "John Smith")
  - Segment inference from contract value
  - Currency cleanup ("$10,000" → 10000.0)
- **Beautiful Terminal UI** - Rich tables and progress bars
- **Type-Safe** - Full Python type hints with modern best practices

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/agentic-data-repair.git
cd agentic-data-repair

# Install with pip
pip install -e .

# Set up API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Usage

```bash
# Generate sample dataset (50 records: 30 clean, 15 fixable, 5 unfixable)
data-repair generate

# Run the repair pipeline
data-repair clean examples/sample_leads.csv

# View results
cat outputs/valid.json      # Clean records
cat outputs/repaired.json   # AI-fixed records
cat outputs/failed.json     # Unrepairable records
```

---

## 📊 Example Output

```
╭─────────────────────────────────────╮
│  Agentic Data Repair                │
│  AI-Powered Data Quality Pipeline   │
╰─────────────────────────────────────╯

Processing: examples/sample_leads.csv

        Processing Results
┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status       ┃ Count ┃ Description          ┃
┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ ✓ Valid      │    30 │ Passed validation    │
│ ⚙ Repaired   │    15 │ Fixed by AI agent    │
│ ✗ Failed     │     5 │ Unrepairable         │
│ Total        │    50 │                      │
└──────────────┴───────┴──────────────────────┘

Success Rate: 90.0%
Results saved to outputs/
```

---

## 🏗️ Architecture

### Pipeline Flow

```
CSV Input → Strict Validation → AI Repair → Structured Output
              ↓ Pass                ↓ Pass        ↓
           valid.json          repaired.json   failed.json
```

### Tech Stack

- **Pydantic AI** - Type-safe LLM agents with structured outputs
- **Google Gemini 2.5 Flash** - Fast, cost-effective AI model
- **Pydantic V2** - Runtime validation with strict mode
- **Typer + Rich** - Professional CLI with beautiful terminal UI

---

## 🔍 Why Pydantic AI?

Unlike raw LLM APIs, Pydantic AI enforces **type safety on AI outputs**:

```python
# Without Pydantic AI - hope the LLM returns valid JSON
response = llm.generate("Fix this data: ...")
data = json.loads(response)  # ❌ Might crash

# With Pydantic AI - guaranteed type safety
result = agent.run_sync("Fix this data: ...")
lead: SalesLead = result.data  # ✅ Type-safe, validated
```

The agent MUST return a valid `SalesLead` object or raise an error. No surprises.

---

## 📝 Schema Example

```python
class SalesLead(BaseModel):
    id: int                           # Positive integer
    name: str                         # Title Case required
    email: EmailStr                   # Valid email format
    country_code: str                 # ISO 3166-1 alpha-2 (e.g., "US")
    segment: Segment                  # Enum: Enterprise/Mid-Market/SMB
    contract_value: float             # Positive currency value
```

**Strict Validation Rules:**
- Names must be in Title Case (enforced by custom validator)
- Country codes must be exactly 2 uppercase letters
- Emails must pass RFC 5322 validation
- Contract values must be positive
- Segments must match enum exactly

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Modern Python** (3.11+, type hints, pyproject.toml)
2. **Pydantic AI agents** with structured outputs
3. **Strict data validation** with Pydantic V2
4. **Professional CLI design** with Typer + Rich
5. **Production patterns** (error handling, logging, file I/O)

---

## 🛠️ Project Structure

```
agentic-data-repair/
├── src/
│   └── data_repair/
│       ├── __init__.py        # Package initialization
│       ├── schemas.py         # Pydantic models
│       ├── agent.py           # Pydantic AI agent
│       ├── processor.py       # Data pipeline
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
├── LICENSE
└── .env.example
```

---

## 📈 Sample Data Distribution

The generated dataset includes:

**30 Clean Records** - Perfect data that passes validation:
- Valid ISO country codes (US, GB, DE, FR, JP, AU, CA, ES)
- Names in proper Title Case
- Valid email addresses
- Correct segment enums
- Positive contract values

**15 Fixable Records** - Issues the AI can repair:
- Country variations: "USA", "usa", "United States", "UK", "germany"
- Name case issues: "alice cooper", "BOB MARLEY"
- Segment variations: "small business", "enterprise"
- Contract formatting: "$45,000", "$200,000.00"

**5 Unfixable Records** - Data that cannot be repaired:
- Empty names
- Invalid email formats
- Negative contract values
- Invalid country codes (ZZZ)
- Missing critical data

---

## 🔧 Advanced Usage

### Custom Output Directory

```bash
data-repair clean input.csv --output custom_results/
```

### Generate Custom Dataset

```bash
data-repair generate --output my_test_data.csv
```

### Environment Variables

```bash
# Set API key directly
export GOOGLE_API_KEY="your_api_key_here"

# Or use .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

---

## 🤝 Contributing

Contributions are welcome! This is a portfolio project designed to demonstrate modern Python and AI best practices.

Areas for improvement:
- Add unit tests with pytest
- Implement async processing for large datasets
- Add confidence scores for repairs
- Support more country code variations
- Add repair statistics and metrics

---

## 📄 License

MIT © 2026 Agentic Data Repair Contributors

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
- [Google Gemini](https://ai.google.dev/) - Powerful language model
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

**Made with ❤️ for the data engineering community**
