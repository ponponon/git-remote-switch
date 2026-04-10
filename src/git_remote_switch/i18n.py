"""Internationalization support for git-remote-switch."""

from __future__ import annotations

import locale
import os


def _is_chinese() -> bool:
    """Detect if the user's locale is Chinese."""
    # Check LANG, LC_ALL, LC_MESSAGES environment variables
    for var in ("LANG", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(var, "")
        if val and ("zh" in val.lower() or "cn" in val.lower()):
            return True

    # Check system locale
    try:
        loc = locale.getdefaultlocale()[0]
        if loc and ("zh" in loc.lower() or "cn" in loc.lower()):
            return True
    except (ValueError, TypeError):
        pass

    try:
        loc = locale.getlocale()[0]
        if loc and ("zh" in loc.lower() or "cn" in loc.lower()):
            return True
    except (ValueError, TypeError):
        pass

    return False


IS_ZH = _is_chinese()


class T:
    """Translation helper — all strings in one place."""

    # App
    app_help: str = "一键切换 Git Remote URL：HTTPS ↔ SSH" if IS_ZH else "Switch git remote URLs between HTTPS and SSH with ease"

    # Arguments / Options
    path_help: str = "Git 仓库路径，默认为当前目录" if IS_ZH else "Path to the git repository. Defaults to current directory."
    dry_run_help: str = "预览模式，不修改 remote" if IS_ZH else "Preview changes without modifying remotes."
    version_help: str = "显示版本号" if IS_ZH else "Show version and exit."

    # Errors / Warnings
    not_git_repo: str = "不是 Git 仓库" if IS_ZH else "is not a git repository"
    no_remotes: str = "未找到 remote。" if IS_ZH else "No remotes found."
    error_prefix: str = "错误" if IS_ZH else "Error"

    # Table headers
    current_remotes: str = "当前 Remote 列表" if IS_ZH else "Current Remotes"
    col_remote: str = "Remote" if IS_ZH else "Remote"
    col_protocol: str = "协议" if IS_ZH else "Protocol"
    col_url: str = "地址" if IS_ZH else "URL"

    # Conversion labels
    https_to_ssh: str = "HTTPS → SSH"
    ssh_to_https: str = "SSH → HTTPS"
    ssh_to_http: str = "SSH → HTTP"

    # SSH prompt
    ssh_prompt: str = "将 SSH 转换为哪种协议？" if IS_ZH else "Convert SSH to which protocol?"
    choice_https: str = "HTTPS (https://...)"
    choice_http: str = "HTTP  (http://...)"

    # Status
    skipped: str = "已跳过" if IS_ZH else "Skipped"
    unsupported_format: str = "不支持的 URL 格式" if IS_ZH else "unsupported URL format"
    dry_run_note: str = "(预览模式，未实际修改)" if IS_ZH else "(dry run, not applied)"
    updated: str = "✓ 已更新" if IS_ZH else "✓ Updated"
    failed_to_update: str = "✗ 更新失败" if IS_ZH else "✗ Failed to update"

    # Summary
    remotes_updated: str = "个 remote 已更新！" if IS_ZH else "remote(s) updated!"
    dry_run_summary: str = "预览模式 — 未做任何修改。" if IS_ZH else "Dry run — no changes made."
    no_changes: str = "无需修改。" if IS_ZH else "No changes needed."
