"""Core logic for git remote URL switching."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class RemoteProtocol(Enum):
    HTTPS = "https"
    HTTP = "http"
    SSH = "ssh"


@dataclass
class RemoteInfo:
    name: str
    url: str
    protocol: RemoteProtocol

    @property
    def is_https(self) -> bool:
        return self.protocol in (RemoteProtocol.HTTPS, RemoteProtocol.HTTP)

    @property
    def is_ssh(self) -> bool:
        return self.protocol == RemoteProtocol.SSH


def is_git_repo(path: Path) -> bool:
    """Check if the given path is inside a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def parse_protocol(url: str) -> RemoteProtocol | None:
    """Detect the protocol of a git remote URL."""
    if url.startswith("https://"):
        return RemoteProtocol.HTTPS
    if url.startswith("http://"):
        return RemoteProtocol.HTTP
    if url.startswith("git@") or url.startswith("ssh://"):
        return RemoteProtocol.SSH
    return None


def get_remotes(repo_path: Path) -> list[RemoteInfo]:
    """Get all remotes for a git repository."""
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    remotes: list[RemoteInfo] = []
    seen: set[str] = set()

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        # Format: "name\turl (fetch)" or "name\turl (push)"
        match = re.match(r"^(\S+)\t(\S+)\s\(fetch\)$", line)
        if not match:
            continue
        name, url = match.group(1), match.group(2)
        if name in seen:
            continue
        seen.add(name)

        protocol = parse_protocol(url)
        if protocol is not None:
            remotes.append(RemoteInfo(name=name, url=url, protocol=protocol))

    return remotes


def https_to_ssh(url: str) -> str:
    """Convert an HTTPS/HTTP URL to SSH format.

    Examples:
        https://github.com/user/repo.git -> git@github.com:user/repo.git
        http://github.com/user/repo.git -> git@github.com:user/repo.git
        https://gitlab.com/org/repo.git -> git@gitlab.com:org/repo.git
    """
    # Strip protocol
    stripped = re.sub(r"^https?://", "", url)
    # Replace first / with :
    parts = stripped.split("/", 1)
    if len(parts) != 2:
        return url
    host, path = parts
    return f"git@{host}:{path}"


def ssh_to_https(url: str, use_http: bool = False) -> str:
    """Convert an SSH URL to HTTPS (or HTTP) format.

    Examples:
        git@github.com:user/repo.git -> https://github.com/user/repo.git
        ssh://git@github.com/user/repo.git -> https://github.com/user/repo.git
    """
    protocol = "http" if use_http else "https"

    # Handle ssh://git@host/path format
    if url.startswith("ssh://"):
        stripped = url[len("ssh://"):]
        if stripped.startswith("git@"):
            stripped = stripped[4:]
        return f"{protocol}://{stripped}"

    # Handle git@host:path format
    if url.startswith("git@"):
        stripped = url[4:]
        # Replace first : with /
        parts = stripped.split(":", 1)
        if len(parts) != 2:
            return url
        host, path = parts
        return f"{protocol}://{host}/{path}"

    return url


def set_remote_url(repo_path: Path, name: str, new_url: str) -> bool:
    """Set a new URL for a git remote."""
    result = subprocess.run(
        ["git", "remote", "set-url", name, new_url],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
