"""CLI interface for git-remote-switch."""

from __future__ import annotations

from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from git_remote_switch.core import (
    get_remotes,
    https_to_ssh,
    is_git_repo,
    set_remote_url,
    ssh_to_https,
)
from git_remote_switch.i18n import T

app = typer.Typer(
    name="git-remote-switch",
    help=T.app_help,
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
        help=T.path_help,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help=T.dry_run_help,
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help=T.version_help,
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    repo_path = path or Path.cwd()

    if not is_git_repo(repo_path):
        console.print(f"[red]{T.error_prefix}:[/red] {repo_path} {T.not_git_repo}")
        raise typer.Exit(1)

    remotes = get_remotes(repo_path)
    if not remotes:
        console.print(f"[yellow]{T.no_remotes}[/yellow]")
        raise typer.Exit(0)

    # Display current remotes
    table = Table(title=T.current_remotes, show_header=True, header_style="bold cyan")
    table.add_column(T.col_remote, style="bold")
    table.add_column(T.col_protocol, style="bold")
    table.add_column(T.col_url)

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
            new_url = https_to_ssh(remote.url)
            console.print(
                f"  [{remote.name}] [green]{T.https_to_ssh}[/green]\n"
                f"    [dim]{remote.url}[/dim]\n"
                f"    → [bold]{new_url}[/bold]"
            )
        elif remote.is_ssh:
            choices = [T.choice_https, T.choice_http]
            answer = questionary.select(
                f"  [{remote.name}] {T.ssh_prompt}",
                choices=choices,
                default=choices[0],
            ).ask()

            if answer is None:
                console.print(f"  [yellow]{T.skipped} {remote.name}[/yellow]")
                continue

            use_http = "HTTP" in answer and "HTTPS" not in answer
            new_url = ssh_to_https(remote.url, use_http=use_http)
            proto_label = T.ssh_to_http if use_http else T.ssh_to_https
            console.print(
                f"  [{remote.name}] [magenta]{proto_label}[/magenta]\n"
                f"    [dim]{remote.url}[/dim]\n"
                f"    → [bold]{new_url}[/bold]"
            )
        else:
            console.print(f"  [yellow]{T.skipped} {remote.name} ({T.unsupported_format})[/yellow]")
            continue

        if new_url and new_url != remote.url:
            if dry_run:
                console.print(f"    [dim]{T.dry_run_note}[/dim]")
            else:
                if set_remote_url(repo_path, remote.name, new_url):
                    console.print(f"    [green]{T.updated}[/green]")
                    changed += 1
                else:
                    console.print(f"    [red]{T.failed_to_update}[/red]")
        console.print()

    # Summary
    if changed > 0:
        console.print(Panel(f"[bold green]{changed} {T.remotes_updated}[/bold green]", expand=False))
    elif dry_run:
        console.print(Panel(f"[bold yellow]{T.dry_run_summary}[/bold yellow]", expand=False))
    else:
        console.print(Panel(f"[bold]{T.no_changes}[/bold]", expand=False))
