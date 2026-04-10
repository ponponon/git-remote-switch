# git-remote-switch

一键切换 Git Remote URL：HTTPS ↔ SSH

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.0.2-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 背景

在国内网络环境下，访问 GitHub 等平台时 HTTPS 方式经常超时或失败，切换到 SSH 可以解决问题；而在公司内网或需要代理时，又可能需要切回 HTTPS。手动改 URL 很麻烦，于是有了这个工具。

## 安装

```bash
pip install git-remote-switch
# 或者
pipx install git-remote-switch
```

对应的 pypi 的地址：[https://pypi.org/manage/project/git-remote-switch](https://pypi.org/manage/project/git-remote-switch)

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
