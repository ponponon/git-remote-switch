"""Tests for git-remote-switch core logic."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from git_remote_switch.core import (
    RemoteInfo,
    RemoteProtocol,
    get_remotes,
    https_to_ssh,
    is_git_repo,
    parse_protocol,
    set_remote_url,
    ssh_to_https,
)


class TestRemoteProtocol:
    """Tests for RemoteProtocol enum."""

    def test_protocol_values(self):
        assert RemoteProtocol.HTTPS.value == "https"
        assert RemoteProtocol.HTTP.value == "http"
        assert RemoteProtocol.SSH.value == "ssh"


class TestRemoteInfo:
    """Tests for RemoteInfo dataclass."""

    def test_is_https(self):
        remote = RemoteInfo(
            name="origin",
            url="https://github.com/user/repo.git",
            protocol=RemoteProtocol.HTTPS,
        )
        assert remote.is_https is True
        assert remote.is_ssh is False

    def test_is_http(self):
        remote = RemoteInfo(
            name="origin",
            url="http://github.com/user/repo.git",
            protocol=RemoteProtocol.HTTP,
        )
        assert remote.is_https is True
        assert remote.is_ssh is False

    def test_is_ssh(self):
        remote = RemoteInfo(
            name="origin",
            url="git@github.com:user/repo.git",
            protocol=RemoteProtocol.SSH,
        )
        assert remote.is_https is False
        assert remote.is_ssh is True


class TestParseProtocol:
    """Tests for parse_protocol function."""

    def test_https(self):
        assert parse_protocol("https://github.com/user/repo.git") == RemoteProtocol.HTTPS

    def test_http(self):
        assert parse_protocol("http://github.com/user/repo.git") == RemoteProtocol.HTTP

    def test_ssh_git(self):
        assert parse_protocol("git@github.com:user/repo.git") == RemoteProtocol.SSH

    def test_ssh_ssh(self):
        assert parse_protocol("ssh://git@github.com/user/repo.git") == RemoteProtocol.SSH

    def test_unknown(self):
        assert parse_protocol("ftp://example.com/repo.git") is None
        assert parse_protocol("invalid-url") is None


class TestHttpsToSsh:
    """Tests for https_to_ssh function."""

    def test_https_github(self):
        url = "https://github.com/user/repo.git"
        expected = "git@github.com:user/repo.git"
        assert https_to_ssh(url) == expected

    def test_http_github(self):
        url = "http://github.com/user/repo.git"
        expected = "git@github.com:user/repo.git"
        assert https_to_ssh(url) == expected

    def test_https_gitlab(self):
        url = "https://gitlab.com/org/repo.git"
        expected = "git@gitlab.com:org/repo.git"
        assert https_to_ssh(url) == expected

    def test_invalid_url(self):
        url = "invalid-url"
        assert https_to_ssh(url) == url

    def test_no_path(self):
        url = "https://github.com"
        assert https_to_ssh(url) == url


class TestSshToHttps:
    """Tests for ssh_to_https function."""

    def test_git_at_format(self):
        url = "git@github.com:user/repo.git"
        expected = "https://github.com/user/repo.git"
        assert ssh_to_https(url) == expected

    def test_ssh_url_format(self):
        url = "ssh://git@github.com/user/repo.git"
        expected = "https://github.com/user/repo.git"
        assert ssh_to_https(url) == expected

    def test_http_option(self):
        url = "git@github.com:user/repo.git"
        expected = "http://github.com/user/repo.git"
        assert ssh_to_https(url, use_http=True) == expected

    def test_invalid_url(self):
        url = "invalid-url"
        assert ssh_to_https(url) == url


class TestIsGitRepo:
    """Tests for is_git_repo function."""

    def test_not_git_repo(self, tmp_path: Path):
        assert is_git_repo(tmp_path) is False

    def test_git_repo(self, tmp_path: Path):
        # Create a fake git repo
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="true\n")
            assert is_git_repo(tmp_path) is True

    def test_git_command_not_found(self):
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            assert is_git_repo(Path("/tmp")) is False


class TestGetRemotes:
    """Tests for get_remotes function."""

    def test_get_remotes_success(self, tmp_path: Path):
        mock_output = "origin\thttps://github.com/user/repo.git (fetch)\n"
        mock_output += "origin\thttps://github.com/user/repo.git (push)\n"
        mock_output += "upstream\tgit@github.com:org/repo.git (fetch)\n"
        mock_output += "upstream\tgit@github.com:org/repo.git (push)\n"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=mock_output)
            remotes = get_remotes(tmp_path)

            assert len(remotes) == 2
            assert remotes[0].name == "origin"
            assert remotes[0].protocol == RemoteProtocol.HTTPS
            assert remotes[1].name == "upstream"
            assert remotes[1].protocol == RemoteProtocol.SSH

    def test_get_remotes_empty(self, tmp_path: Path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="")
            remotes = get_remotes(tmp_path)
            assert remotes == []

    def test_get_remotes_error(self, tmp_path: Path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
            remotes = get_remotes(tmp_path)
            assert remotes == []


class TestSetRemoteUrl:
    """Tests for set_remote_url function."""

    def test_set_remote_url_success(self, tmp_path: Path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = set_remote_url(tmp_path, "origin", "https://new-url.com/repo.git")
            assert result is True
            mock_run.assert_called_once_with(
                ["git", "remote", "set-url", "origin", "https://new-url.com/repo.git"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )

    def test_set_remote_url_failure(self, tmp_path: Path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = set_remote_url(tmp_path, "origin", "https://new-url.com/repo.git")
            assert result is False
