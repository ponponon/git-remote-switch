"""Tests for git-remote-switch CLI."""

from unittest.mock import patch

from typer.testing import CliRunner

from git_remote_switch.cli import app

runner = CliRunner()


def test_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "git-remote-switch" in result.output


def test_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for help content (typer shows usage info)
    assert "Usage" in result.output or "OPTIONS" in result.output


def test_not_git_repo(tmp_path):
    """Test running on a non-git directory."""
    result = runner.invoke(app, [str(tmp_path)])
    assert result.exit_code == 1
    assert "git" in result.output.lower() or "repo" in result.output.lower()


def test_dry_run(tmp_path):
    """Test --dry-run flag on a non-git directory (should still fail gracefully)."""
    result = runner.invoke(app, [str(tmp_path), "--dry-run"])
    # Should still exit with error since it's not a git repo
    assert result.exit_code == 1


def test_no_remotes_mocked(tmp_path):
    """Test when there are no remotes configured."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    with (
        patch("git_remote_switch.cli.is_git_repo", return_value=True),
        patch("git_remote_switch.cli.get_remotes", return_value=[]),
    ):
        result = runner.invoke(app, [str(tmp_path)])
        assert result.exit_code == 0


def test_with_remotes_mocked(tmp_path):
    """Test with mocked remotes."""
    from git_remote_switch.core import RemoteInfo, RemoteProtocol
    
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    mock_remotes = [
        RemoteInfo(
            name="origin",
            url="https://github.com/user/repo.git",
            protocol=RemoteProtocol.HTTPS,
        )
    ]
    
    with (
        patch("git_remote_switch.cli.is_git_repo", return_value=True),
        patch("git_remote_switch.cli.get_remotes", return_value=mock_remotes),
        patch(
            "git_remote_switch.cli.https_to_ssh",
            return_value="git@github.com:user/repo.git",
        ),
        patch("git_remote_switch.cli.set_remote_url", return_value=True),
    ):
        # Simulate user selection by providing input
        result = runner.invoke(app, [str(tmp_path)], input="\n")
        # Should complete successfully
        assert result.exit_code == 0
