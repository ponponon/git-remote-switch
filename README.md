# git-remote-switch

一键切换 Git Remote URL：HTTPS ↔ SSH

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.0.2-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <a href="https://github.com/ponponon/git-remote-switch/actions/workflows/ci.yml"><img src="https://github.com/ponponon/git-remote-switch/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/git-remote-switch/"><img src="https://img.shields.io/pypi/dm/git-remote-switch" alt="PyPI Downloads"></a>
</p>

---

## 📖 目录

- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [工作原理](#工作原理)
- [示例演示](#示例演示)
- [常见问题](#常见问题)
- [贡献](#贡献)
- [许可证](#许可证)

## 背景

在国内网络环境下，访问 GitHub 等平台时 HTTPS 方式经常超时或失败，切换到 SSH 可以解决问题；而在公司内网或需要代理时，又可能需要切回 HTTPS。手动改 URL 很麻烦，于是有了这个工具。

## 安装

### 使用 pip

```bash
pip install git-remote-switch
```

### 使用 pipx（推荐）

```bash
pipx install git-remote-switch
```

### 从源码安装

```bash
git clone https://github.com/ponponon/git-remote-switch.git
cd git-remote-switch
pip install -e .
```

📦 PyPI: [https://pypi.org/project/git-remote-switch](https://pypi.org/project/git-remote-switch)

## 使用

### 基本用法

```bash
# 切换当前目录的 remote
git-remote-switch

# 或使用简写
grs
```

### 指定目录

```bash
# 切换指定目录的 remote
git-remote-switch /path/to/repo
```

### 预览模式

```bash
# 只查看变更，不实际修改
git-remote-switch --dry-run

# 或使用简写
grs -n
```

### 查看版本

```bash
git-remote-switch --version
```

### 查看帮助

```bash
git-remote-switch --help
```

## 工作原理

- 如果 remote URL 是 **HTTPS/HTTP**，自动转换为 **SSH** 格式
- 如果 remote URL 是 **SSH**，会让你选择转换为 **HTTPS** 还是 **HTTP**

### URL 转换示例

| 原始 URL | 转换后 |
|----------|--------|
| `https://github.com/user/repo.git` | `git@github.com:user/repo.git` |
| `http://github.com/user/repo.git` | `git@github.com:user/repo.git` |
| `git@github.com:user/repo.git` | `https://github.com/user/repo.git`（可选择） |
| `ssh://git@github.com/user/repo.git` | `https://github.com/user/repo.git` |

### 支持的平台

- GitHub
- GitLab
- Gitee
- Bitbucket
- 任何标准 Git 托管服务

## 示例演示

### 场景 1：HTTPS → SSH

```bash
$ cd ~/projects/my-repo
$ grs

Current Remotes
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name   ┃ Protocol  ┃ URL                                ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ origin │ https     │ https://github.com/user/repo.git   │
└────────┴───────────┴────────────────────────────────────┘

  [origin] Converting HTTPS to SSH...
    https://github.com/user/repo.git
    → git@github.com:user/repo.git
    ✅ Updated!

╭─────────────────────────────╮
│ 1 remote(s) updated        │
╰─────────────────────────────╯
```

### 场景 2：SSH → HTTPS

```bash
$ grs

Current Remotes
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name   ┃ Protocol  ┃ URL                                ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ origin │ ssh       │ git@github.com:user/repo.git       │
└────────┴───────────┴────────────────────────────────────┘

  [origin] Convert SSH to?
  ❯ HTTPS
    HTTP

  [origin] Converting SSH to HTTPS...
    git@github.com:user/repo.git
    → https://github.com/user/repo.git
    ✅ Updated!
```

### 场景 3：预览模式

```bash
$ grs --dry-run

  [origin] Converting HTTPS to SSH...
    https://github.com/user/repo.git
    → git@github.com:user/repo.git
    ℹ️ Dry run - no changes made

╭─────────────────────────────╮
│ Dry run completed          │
╰─────────────────────────────╯
```

## 常见问题

### Q: 为什么切换后还需要输入密码？

A: SSH 方式需要使用 SSH 密钥。请确保你已经生成并配置了 SSH 密钥：

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到 GitHub/GitLab 等平台
cat ~/.ssh/id_ed25519.pub
```

### Q: 可以批量处理多个仓库吗？

A: 目前不支持，但你可以在父目录中使用循环：

```bash
for dir in */; do
  echo "Processing $dir..."
  (cd "$dir" && grs --dry-run)
done
```

### Q: 支持多个 remote 吗？

A: 是的！会自动处理 `origin`、`upstream` 等所有 remote。

### Q: 如何撤销操作？

A: 再次运行 `grs` 即可切换回来。或者使用 Git 命令：

```bash
git remote set-url origin <original-url>
```

### Q: 为什么我的 URL 没有被识别？

A: 目前支持以下格式：
- `https://host/path/to/repo.git`
- `http://host/path/to/repo.git`
- `git@host:path/to/repo.git`
- `ssh://git@host/path/to/repo.git`

如果遇到其他格式，请提交 Issue。

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 快速开始

```bash
# Fork 并克隆
git clone https://github.com/YOUR_USERNAME/git-remote-switch.git
cd git-remote-switch

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 检查代码风格
ruff check src/ tests/
```

## 相关项目

- [Typer](https://typer.tiangolo.com/) - CLI 框架
- [Rich](https://rich.readthedocs.io/) - 终端美化库
- [Questionary](https://questionary.readthedocs.io/) - 交互式提示库

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

Made with ❤️ by ponponon
