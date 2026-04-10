"""CLI interface for git-remote-switch."""

from __future__ import annotations

from pathlib import Path


import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from git_remote_switch.core import (
    RemoteProtocol,
    get_remotes,
    https_to_ssh,
    is_git_repo,
    set_remote_url,
    ssh_to_https,
)

app = typer.Typer(
    name="git-remote-switch",
    help="Switch git remote URLs between HTTPS and SSH with ease.",
    no_args_is_help=False,
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        from git_remote_switch import __version__
        console.print(f"git-remote-switch {__version__}")
        raise typer.Exit()


@app.command()
def main(
    path: Path | None = typer.Argument(
        None,
        help="Path to the git repository. Defaults to current directory.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Preview changes without modifying remotes.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Switch git remote URLs between HTTPS and SSH."""
    repo_path = path or Path.cwd()

    if not is_git_repo(repo_path):
        console.print(f"[red]Error:[/red] {repo_path} is not a git repository")
        raise typer.Exit(1)

    remotes = get_remotes(repo_path)
    if not remotes:
        console.print("[yellow]No remotes found.[/yellow]")
        raise typer.Exit(0)

    # Display current remotes
    table = Table(title="Current Remotes", show_header=True, header_style="bold cyan")
    table.add_column("Remote", style="bold")
    table.add_column("Protocol", style="bold")
    table.add_column("URL")

    for r in remotes:
        proto_style = "green" if r.is_https else "magenta"
        table.add_row(r.name, f"[{proto_style}]{r.protocol.value}[/{proto_style}]", r.url)

    console.print(table)
    console.print()

    # Process each remote
    changed = 0
    for remote in remotes:
        new_url: str | None = None

        if remote.is_https:
            # HTTPS/HTTP -> SSH
            new_url = https_to_ssh(remote.url)
            console.print(
                f"  [{remote.name}] [green]HTTPS → SSH[/green]\n"
                f"    [dim]{remote.url}[/dim]\n"
                f"    → [bold]{new_url}[/bold]"
            )
        elif remote.is_ssh:
            # SSH -> HTTPS or HTTP (user choice)
            choices = [
                f"HTTPS (https://...)",
                f"HTTP  (http://...)",
            ]
            answer = questionary.select(
                f"  [{remote.name}] Convert SSH to which protocol?",
                choices=choices,
                default=choices[0],
            ).ask()

            if answer is None:
                console.print(f"  [yellow]Skipped {remote.name}[/yellow]")
                continue

            use_http = "HTTP" in answer
            new_url = ssh_to_https(remote.url, use_http=use_http)
            proto_label = "HTTP" if use_http else "HTTPS"
            console.print(
                f"  [{remote.name}] [magenta]SSH → {proto_label}[/magenta]\n"
                f"    [dim]{remote.url}[/dim]\n"
                f"    → [bold]{new_url}[/bold]"
            )
        else:
            console.print(f"  [yellow]Skipped {remote.name} (unsupported URL format)[/yellow]")
            continue

        if new_url and new_url != remote.url:
            if dry_run:
                console.print(f"    [dim](dry run, not applied)[/dim]")
            else:
                if set_remote_url(repo_path, remote.name, new_url):
                    console.print(f"    [green]✓ Updated[/green]")
                    changed += 1
                else:
                    console.print(f"    [red]✗ Failed to update[/red]")
        console.print()

    # Summary
    if changed > 0:
        console.print(Panel(f"[bold green]{changed} remote(s) updated![/bold green]", expand=False))
    elif dry_run:
        console.print(Panel("[bold yellow]Dry run — no changes made.[/bold yellow]", expand=False))
    else:
        console.print(Panel("[bold]No changes needed.[/bold]", expand=False))
