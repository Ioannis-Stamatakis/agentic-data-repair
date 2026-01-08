"""CLI interface with Rich terminal UI."""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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
    console.print(f"\n[bold]Processing:[/bold] {input_csv}\n")
    processor = DataProcessor()
    processor.process_csv(str(input_csv))

    # Save results
    processor.save_results(str(output_dir))

    # Summary table
    table = Table(title="\n[bold]Processing Results[/bold]", show_header=True)
    table.add_column("Status", style="bold", width=15)
    table.add_column("Count", justify="right", style="cyan", width=10)
    table.add_column("Description", style="dim")

    total = (
        len(processor.valid_leads) +
        len(processor.repaired_leads) +
        len(processor.failed_leads)
    )

    table.add_row(
        "[green]✓ Valid[/green]",
        str(len(processor.valid_leads)),
        "Passed strict validation"
    )
    table.add_row(
        "[yellow]⚙ Repaired[/yellow]",
        str(len(processor.repaired_leads)),
        "Fixed by AI agent"
    )
    table.add_row(
        "[red]✗ Failed[/red]",
        str(len(processor.failed_leads)),
        "Unrepairable records"
    )
    table.add_row(
        "[bold]Total[/bold]",
        f"[bold]{total}[/bold]",
        ""
    )

    console.print(table)

    # Success rate
    success_rate = (
        (len(processor.valid_leads) + len(processor.repaired_leads)) / total * 100
    ) if total > 0 else 0
    console.print(f"\n[bold green]Success Rate:[/bold green] {success_rate:.1f}%")
    console.print(f"[dim]Results saved to {output_dir}/[/dim]\n")


@app.command()
def generate(
    output_file: Path = typer.Option(
        "examples/sample_leads.csv",
        "--output", "-o",
        help="Output CSV file path"
    )
):
    """Generate sample dataset with clean and messy records.

    Creates a 50-row CSV file with:
    - 30 clean records (perfect data)
    - 15 fixable records (AI can repair)
    - 5 unfixable records (will fail)

    Example:
        $ data-repair generate
        $ data-repair generate --output test_data.csv
    """
    from .generator import generate_sample_data

    output_file.parent.mkdir(parents=True, exist_ok=True)
    generate_sample_data(str(output_file))

    console.print(
        f"[green]✓[/green] Generated 50 sample records at [cyan]{output_file}[/cyan]"
    )
    console.print("[dim]Distribution: 30 clean, 15 fixable, 5 unfixable[/dim]")


if __name__ == "__main__":
    app()
