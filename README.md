# git-remote-switch

Switch git remote URLs between HTTPS and SSH with ease.

## Installation

```bash
pip install git-remote-switch
# or
pipx install git-remote-switch
```

## Usage

```bash
# Switch remotes in current directory
git-remote-switch
# or use the short alias
grs

# Switch remotes in a specific directory
git-remote-switch /path/to/repo

# Dry run (preview without making changes)
git-remote-switch --dry-run
```

## How it works

- If a remote URL uses **HTTPS/HTTP**, it will be converted to **SSH** format
- If a remote URL uses **SSH**, you'll be prompted to choose between **HTTPS** or **HTTP**

### URL Conversion Examples

| From | To |
|------|----|
| `https://github.com/user/repo.git` | `git@github.com:user/repo.git` |
| `http://github.com/user/repo.git` | `git@github.com:user/repo.git` |
| `git@github.com:user/repo.git` | `https://github.com/user/repo.git` (your choice) |

## License

MIT
