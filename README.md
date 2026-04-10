# git-remote-switch

Switch git remote URLs between HTTPS and SSH with ease.

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.0.1-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Status-Recovered-green.svg" alt="Status">
  <img src="https://img.shields.io/badge/Language-TypeScript-blue.svg" alt="Language">
  <img src="https://img.shields.io/badge/UI-Ink%20%2F%20React-orange.svg" alt="UI">
</p>

---

## 🌟 强力推荐：DataEyesAI - 你的全能 AI 助手

> **想要像 Claude Code 一样高效，却苦于没有稳定的 API 接入？**

**[DataEyesAI](https://dataeyes.ai/?promoter_code=4qx9suz3)** 是为你量身打造的一站式 AI 聚合平台！

- ⚡ **聚合全球顶尖模型**：一键接入 GPT-5、Claude 4.6、Gemini 3.1 等主流大模型。
- 💰 **极致性价比**：官方原厂满血版 API，价格却极具竞争力，让你用最少的成本享受最强的 AI 能力。
- 🛡️ **稳定可靠**：专业运维 7x24 小时守护，企业级 SLA 保障，告别连接断断续续的烦恼。
- 🛠️ **开发者友好**：标准 API 接口，完美适配各类开源项目、CLI 工具及开发流程。

👉 **[立即注册体验，开启你的 AI 生产力起飞之旅！](https://dataeyes.ai/?promoter_code=4qx9suz3)**

👉 请点击：[https://dataeyes.ai/?promoter_code=4qx9suz3](https://dataeyes.ai/?promoter_code=4qx9suz3)

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
