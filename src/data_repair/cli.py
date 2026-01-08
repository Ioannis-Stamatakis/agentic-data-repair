"""CLI interface with Rich terminal UI."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.text import Text

from .processor import DataProcessor

app = typer.Typer(
    name="data-repair",
    help="AI-powered self-healing data pipeline using Pydantic AI",
    add_completion=False
)
console = Console()


@app.command()
def clean(
    input_csv: Path = typer.Argument(
        ...,
        help="Path to input CSV file",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output_dir: Path = typer.Option(
        "outputs",
        "--output", "-o",
        help="Directory for output JSON files"
    )
):
    """Clean and repair sales lead data using AI-powered validation.

    Outputs 3 JSON files:
    - valid.json: Records that passed validation
    - repaired.json: Records fixed by AI agent
    - failed.json: Unrepairable records

    Example:
        $ data-repair clean examples/sample_leads.csv
        $ data-repair clean input.csv --output results/
    """
    # Header
    console.print(Panel.fit(
        "[bold cyan]Agentic Data Repair[/bold cyan]\n"
        "AI-Powered Data Quality Pipeline",
        border_style="cyan"
    ))

    # Process data
    console.print(f"\n[bold cyan]Dataset:[/bold cyan] {input_csv}")
    console.print(f"[bold cyan]AI Model:[/bold cyan] Gemini 2.5 Flash")
    console.print(f"[bold cyan]Mode:[/bold cyan] 3-Stage Pipeline (Validate → Repair → Report)\n")

    processor = DataProcessor()
    processor.process_csv(str(input_csv))

    # Save results
    processor.save_results(str(output_dir))

    # Calculate metrics
    total = (
        len(processor.valid_leads) +
        len(processor.repaired_leads) +
        len(processor.failed_leads)
    )
    success_rate = (
        (len(processor.valid_leads) + len(processor.repaired_leads)) / total * 100
    ) if total > 0 else 0

    # Summary table with enhanced styling
    console.print()
    table = Table(
        title="[bold white]PIPELINE RESULTS[/bold white]",
        show_header=True,
        border_style="cyan",
        title_style="bold cyan",
        show_lines=True
    )
    table.add_column("Category", style="bold", width=20)
    table.add_column("Count", justify="right", style="bold cyan", width=10)
    table.add_column("Percentage", justify="right", style="dim", width=12)
    table.add_column("Status", style="dim")

    table.add_row(
        "[green]✓ Valid[/green]",
        f"[green]{len(processor.valid_leads)}[/green]",
        f"[green]{len(processor.valid_leads)/total*100:.1f}%[/green]" if total > 0 else "0%",
        "Passed strict validation"
    )
    table.add_row(
        "[yellow]⚙ Repaired by AI[/yellow]",
        f"[yellow]{len(processor.repaired_leads)}[/yellow]",
        f"[yellow]{len(processor.repaired_leads)/total*100:.1f}%[/yellow]" if total > 0 else "0%",
        "Fixed by Gemini agent"
    )
    table.add_row(
        "[red]✗ Failed[/red]",
        f"[red]{len(processor.failed_leads)}[/red]",
        f"[red]{len(processor.failed_leads)/total*100:.1f}%[/red]" if total > 0 else "0%",
        "Unrepairable records"
    )
    table.add_row(
        "[bold]━━━━━━━━━━━━━━━━━━[/bold]",
        "[bold]━━━━━━[/bold]",
        "[bold]━━━━━━━━━[/bold]",
        "[bold]━━━━━━━━━━━━━━━━━━━━[/bold]"
    )
    table.add_row(
        "[bold white]TOTAL PROCESSED[/bold white]",
        f"[bold white]{total}[/bold white]",
        "[bold white]100.0%[/bold white]",
        ""
    )

    console.print(table)

    # Success rate panel
    if success_rate >= 90:
        rate_color = "green"
        status = "EXCELLENT"
    elif success_rate >= 75:
        rate_color = "yellow"
        status = "GOOD"
    else:
        rate_color = "red"
        status = "NEEDS IMPROVEMENT"

    console.print()
    console.print(Panel(
        f"[bold {rate_color}]SUCCESS RATE: {success_rate:.1f}% - {status}[/bold {rate_color}]\n"
        f"[dim]Data Quality: {len(processor.valid_leads) + len(processor.repaired_leads)}/{total} records compliant with schema[/dim]",
        border_style=rate_color,
        title="[bold]QUALITY SCORE[/bold]",
        title_align="left"
    ))

    # Show example repairs if any
    if processor.repaired_leads and len(processor.repaired_leads) > 0:
        console.print()
        repair_table = Table(
            title="[bold yellow]AI REPAIR EXAMPLES[/bold yellow]",
            show_header=True,
            border_style="yellow",
            title_style="bold yellow"
        )
        repair_table.add_column("Record ID", style="bold white", width=10)
        repair_table.add_column("Field", style="bold cyan", width=14)
        repair_table.add_column("Original Value", style="red", width=28)
        repair_table.add_column("Repaired Value", style="green", width=28)
        repair_table.add_column("Fix Type", style="dim", width=18)

        # Collect all repairs to show variety
        repairs_shown = 0
        max_repairs = 8  # Show up to 8 examples

        for repair in processor.repaired_leads:
            if repairs_shown >= max_repairs:
                break

            original = repair['original']
            fixed = repair['repaired']
            record_id = original.get('id', '?')

            # Find what changed
            if original.get('country_code') != fixed.get('country_code'):
                repair_table.add_row(
                    str(record_id),
                    "country_code",
                    f"{original['country_code']}",
                    f"{fixed['country_code']}",
                    "Country ISO code"
                )
                repairs_shown += 1
            if original.get('name') != fixed.get('name'):
                repair_table.add_row(
                    str(record_id),
                    "name",
                    f"{original['name']}",
                    f"{fixed['name']}",
                    "Title case"
                )
                repairs_shown += 1
            if original.get('segment') != fixed.get('segment'):
                # Handle both string and enum values for segment
                fixed_segment = fixed['segment']
                if hasattr(fixed_segment, 'value'):
                    fixed_segment = fixed_segment.value
                repair_table.add_row(
                    str(record_id),
                    "segment",
                    f"{original['segment']}",
                    f"{fixed_segment}",
                    "Segment mapping"
                )
                repairs_shown += 1

        console.print(repair_table)

    # Footer
    console.print()
    console.print(f"[bold]Output Files:[/bold]")
    console.print(f"  [cyan]→[/cyan] {output_dir}/valid.json - Clean records")
    console.print(f"  [cyan]→[/cyan] {output_dir}/repaired.json - AI-fixed records")
    console.print(f"  [cyan]→[/cyan] {output_dir}/failed.json - Unrepairable records")
    console.print()
    console.print(f"[dim]Powered by: Pydantic AI + Google Gemini 2.5 Flash[/dim]\n")


@app.command()
def generate(
    output_file: Path = typer.Option(
        "examples/sample_leads.csv",
        "--output", "-o",
        help="Output CSV file path"
    ),
    size: int = typer.Option(
        50,
        "--size", "-s",
        help="Number of records to generate",
        min=10,
        max=10000
    )
):
    """Generate sample dataset with clean and messy records.

    Distribution:
    - 60% clean records (perfect data)
    - 30% fixable records (AI can repair)
    - 10% unfixable records (will fail)

    Example:
        $ data-repair generate
        $ data-repair generate --size 200
        $ data-repair generate --output test_data.csv --size 500
    """
    from .generator import generate_sample_data

    output_file.parent.mkdir(parents=True, exist_ok=True)
    generate_sample_data(str(output_file), size=size)

    clean_count = int(size * 0.60)
    fixable_count = int(size * 0.30)
    unfixable_count = size - clean_count - fixable_count

    console.print(
        f"[green]✓[/green] Generated {size} sample records at [cyan]{output_file}[/cyan]"
    )
    console.print(
        f"[dim]Distribution: {clean_count} clean, {fixable_count} fixable, "
        f"{unfixable_count} unfixable[/dim]"
    )


if __name__ == "__main__":
    app()
