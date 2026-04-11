# Contributing to git-remote-switch

首先，感谢你愿意为 `git-remote-switch` 做出贡献！🎉

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [代码风格](#代码风格)
- [测试](#测试)
- [提交 PR](#提交-pr)
- [报告 Bug](#报告-bug)
- [功能建议](#功能建议)

## 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。请尊重所有贡献者和用户。

## 如何贡献

你可以通过以下方式贡献：

1. **报告 Bug** - 提交 Issue
2. **功能建议** - 提交 Issue 并标注为 enhancement
3. **修复 Bug** - Fork 仓库，创建分支，提交 PR
4. **添加功能** - 先开 Issue 讨论，再实现
5. **改进文档** - 直接提交 PR
6. **翻译** - 帮助完善 i18n 支持

## 开发环境设置

### 1. Fork 并克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/git-remote-switch.git
cd git-remote-switch
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

### 3. 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 4. 验证安装

```bash
# 运行测试
pytest tests/ -v

# 检查代码风格
ruff check src/ tests/
```

## 代码风格

本项目使用以下工具保持代码质量：

- **Ruff** - 快速的 Python linter
- **类型注解** - 所有公共函数和类都需要类型注解

### 代码规范

```python
# ✅ 好的做法
def https_to_ssh(url: str) -> str:
    """Convert an HTTPS URL to SSH format."""
    ...

# ❌ 避免
def convert_url(url):  # 缺少类型注解和文档字符串
    ...
```

### 运行 Lint

```bash
ruff check src/ tests/
ruff format src/ tests/  # 如果需要格式化
```

## 测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试文件

```bash
pytest tests/test_core.py -v
```

### 查看覆盖率

```bash
pytest tests/ --cov=git_remote_switch --cov-report=term-missing
```

### 编写测试

- 单元测试放在 `tests/` 目录下
- 测试函数以 `test_` 开头
- 使用 `pytest` 的 `tmp_path` fixture 创建临时目录
- Mock 外部依赖（如 subprocess）

示例：

```python
def test_https_to_ssh():
    url = "https://github.com/user/repo.git"
    expected = "git@github.com:user/repo.git"
    assert https_to_ssh(url) == expected
```

## 提交 PR

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-123
```

### 2. 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 添加新功能
fix: 修复 Bug
docs: 更新文档
style: 代码格式调整
refactor: 重构代码
test: 添加测试
chore: 构建/工具相关
```

示例：

```bash
git commit -m "feat: 添加 GitLab 云原生支持"
git commit -m "fix: 修复 HTTP 协议检测逻辑"
```

### 3. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

### PR 要求

- [ ] 代码通过所有测试
- [ ] 添加了必要的单元测试
- [ ] 代码通过 Ruff 检查
- [ ] 更新了文档（如需要）
- [ ] 更新了 CHANGELOG.md（如需要）

## 报告 Bug

提交 Issue 时请包含：

1. **问题描述** - 清晰描述发生了什么
2. **复现步骤**
   ```bash
   # 1. 执行什么命令
   git-remote-switch /path/to/repo
   
   # 2. 看到什么错误
   ```
3. **预期行为** - 应该发生什么
4. **环境信息**
   - Python 版本：`python --version`
   - git-remote-switch 版本：`git-remote-switch --version`
   - 操作系统：Windows/macOS/Linux

## 功能建议

欢迎提出新功能建议！提交 Issue 时请说明：

1. **功能描述** - 你想要什么功能
2. **使用场景** - 为什么需要这个功能
3. **实现思路**（可选）- 你有什么想法

---

再次感谢你的贡献！🙏
