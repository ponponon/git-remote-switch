# git-remote-switch

一键切换 Git Remote URL：HTTPS ↔ SSH

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
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

## 背景

在国内网络环境下，访问 GitHub 等平台时 HTTPS 方式经常超时或失败，切换到 SSH 可以解决问题；而在公司内网或需要代理时，又可能需要切回 HTTPS。手动改 URL 很麻烦，于是有了这个工具。

## 安装

```bash
pip install git-remote-switch
# 或者
pipx install git-remote-switch
```

## 使用

```bash
# 切换当前目录的 remote
git-remote-switch
# 或者用简写
grs

# 指定目录
git-remote-switch /path/to/repo

# 预览模式（只看不改）
git-remote-switch --dry-run
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

## 许可证

MIT
