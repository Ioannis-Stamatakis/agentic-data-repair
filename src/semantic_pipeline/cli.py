"""CLI interface with Rich terminal UI."""

import typer
from pathlib import Path
from importlib.metadata import version as get_version, PackageNotFoundError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.text import Text

from .processor import DataProcessor


def get_app_version() -> str:
    """Get the application version from package metadata."""
    try:
        return get_version("semantic-data-pipeline-agent")
    except PackageNotFoundError:
        return "2.0.0"  # Fallback for development


def version_callback(value: bool):
    """Display version information and exit."""
    if value:
        console.print(f"[bold cyan]Semantic Data Pipeline Agent[/bold cyan] v{get_app_version()}")
        console.print("[dim]AI-Powered Semantic Extraction using Pydantic AI + Google Gemini[/dim]")
        raise typer.Exit()


app = typer.Typer(
    name="pipeline",
    help="Semantic data extraction pipeline - transforms unstructured text to structured data",
    add_completion=False
)
console = Console()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """Semantic Data Pipeline Agent - AI-powered data extraction."""
    pass


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
    ),
    min_confidence: float = typer.Option(
        0.0,
        "--min-confidence", "-c",
        help="Minimum confidence score (0.0-1.0) for repaired records. Records below this threshold are saved separately to low_confidence.json",
        min=0.0,
        max=1.0
    )
):
    """Extract structured data from unstructured text using AI.

    Outputs 3 JSON files:
    - valid.json: Records that passed validation
    - repaired.json: Records with AI-extracted fields
    - failed.json: Unrepairable records

    Example:
        $ pipeline clean examples/sample_leads.csv
        $ pipeline clean input.csv --output results/
    """
    # Header
    console.print(Panel.fit(
        "[bold cyan]Semantic Data Pipeline Agent[/bold cyan]\n"
        "AI-Powered Semantic Extraction",
        border_style="cyan"
    ))

    # Process data
    console.print(f"\n[bold cyan]Dataset:[/bold cyan] {input_csv}")
    console.print(f"[bold cyan]AI Model:[/bold cyan] Gemini 2.5 Flash")
    console.print(f"[bold cyan]Mode:[/bold cyan] Semantic Extraction Pipeline (Validate → Extract → Report)\n")

    if min_confidence > 0.0:
        console.print(f"[bold cyan]Min Confidence:[/bold cyan] {min_confidence:.0%}\n")

    processor = DataProcessor(min_confidence=min_confidence)
    processor.process_csv(str(input_csv))

    # Save results
    processor.save_results(str(output_dir))

    # Calculate metrics
    total = (
        len(processor.valid_leads) +
        len(processor.repaired_leads) +
        len(processor.low_confidence_leads) +
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
    if processor.low_confidence_leads:
        table.add_row(
            "[magenta]⚠ Low Confidence[/magenta]",
            f"[magenta]{len(processor.low_confidence_leads)}[/magenta]",
            f"[magenta]{len(processor.low_confidence_leads)/total*100:.1f}%[/magenta]" if total > 0 else "0%",
            f"Below {min_confidence:.0%} threshold"
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

    # Show semantic extraction examples if any
    if processor.repaired_leads and len(processor.repaired_leads) > 0:
        console.print()
        extraction_table = Table(
            title="[bold yellow]SEMANTIC EXTRACTION EXAMPLES[/bold yellow]",
            show_header=True,
            border_style="yellow",
            title_style="bold yellow"
        )
        extraction_table.add_column("ID", style="bold white", width=5)
        extraction_table.add_column("Input Note", style="dim", width=60, no_wrap=False)
        extraction_table.add_column("Country", style="green", width=8)
        extraction_table.add_column("Industry", style="cyan", width=10)
        extraction_table.add_column("Value (USD)", style="green", width=12)
        extraction_table.add_column("Confidence", style="yellow", width=10)

        # Show up to 5 successful extraction examples
        extractions_shown = 0
        max_extractions = 5

        for repair in processor.repaired_leads:
            if extractions_shown >= max_extractions:
                break

            original = repair['original']
            fixed = repair['repaired']
            record_id = original.get('id', '?')

            # Only show if semantic extraction SUCCEEDED (sales_notes present AND fields extracted)
            if original.get('sales_notes'):
                country = fixed.get('country_code')
                industry = fixed.get('industry')
                value = fixed.get('contract_value')

                # Skip if extraction failed (no fields were populated)
                if not country and not industry and not value:
                    continue

                # Use full note (no truncation, will wrap automatically)
                note = original['sales_notes']

                # Format extracted fields
                country_str = country if country else "N/A"

                if hasattr(industry, 'value'):
                    industry_str = industry.value
                else:
                    industry_str = industry if industry else "N/A"

                value_str = f"${value:,.0f}" if value else "N/A"

                confidence = fixed.get('confidence_score', 0.0)
                confidence_str = f"{confidence:.1%}"

                extraction_table.add_row(
                    str(record_id),
                    note,
                    country_str,
                    industry_str,
                    value_str,
                    confidence_str
                )
                extractions_shown += 1

        # Only show table if we have successful extractions
        if extractions_shown > 0:
            console.print(extraction_table)

    # Footer
    console.print()
    console.print(f"[bold]Output Files:[/bold]")
    console.print(f"  [cyan]→[/cyan] {output_dir}/valid.json - Clean records")
    console.print(f"  [cyan]→[/cyan] {output_dir}/repaired.json - AI-fixed records")
    if processor.low_confidence_leads:
        console.print(f"  [cyan]→[/cyan] {output_dir}/low_confidence.json - Below {min_confidence:.0%} threshold")
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
