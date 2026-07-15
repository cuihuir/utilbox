# UtilBox Handoff

最后更新：2026-07-15

## 当前状态

- 分支：`master`，工作区干净。
- 最新提交：`0382e05 chore: release version 1.1.3`。
- 最新 Release：[`v1.1.3`](https://github.com/cuihuir/utilbox/releases/tag/v1.1.3)。
- `v1.1.3` 的全平台构建已成功：Windows ZIP、macOS app ZIP、Linux DEB/AppImage、Fedora RPM。
- 最近一次完整构建：<https://github.com/cuihuir/utilbox/actions/runs/29419328445>。

## 版本与发布

`VERSION` 是唯一版本源。界面显示、Python 包元数据、冻结程序、DEB、RPM 和 AppImage 都从这里派生。

发布流程：

1. 只修改 `VERSION`，例如改为 `1.1.4`。
2. 运行 `uv lock` 和 `uv run python -m unittest tests/test_version.py`。
3. 提交并推送 `master`。
4. 创建同名标签的 Release：`v1.1.4`。工作流会拒绝 tag 与 `VERSION` 不一致的 Release。
5. 等待 GitHub Actions 的 `Build release packages` 完成后，再下载并测试对应平台产物。

创建 Release 时不要把字面量 `\n` 传给 `gh release create --notes`；GitHub 会原样显示它。应使用真实 Markdown 文件：

```bash
gh release create v1.1.4 --target master --title "UtilBox v1.1.4" --notes-file /path/to/release-notes.md
```

## 打包要点

- 发布工作流：`.github/workflows/release.yml`。
- Linux 使用固定的 `.venv/bin/python` 和 `.venv/bin/pyinstaller`；不要在 `uv sync --python ...` 后改用裸 `uv run`，否则可能回退到 `.python-version` 指定的 Python 3.14，导致 Tcl/Tk 路径为空。
- Linux 冻结程序明确打包 Tcl/Tk 动态库，并在 CI 里用 `xvfb-run` 启动检查。
- AppImage 需要宿主 FUSE 才能直接挂载；无 FUSE 时可用 `--appimage-extract-and-run`。
- 在 Debian 12 Distrobox 已实际验证：冻结二进制、DEB 安装后的 `utilbox` 命令、以及 AppImage 的解压运行模式均可启动。

## 图标与界面

- 当前应用 Logo 是蓝底白色 `U`：`src/assets/icons/utilbox.svg`。
- 对应 PNG 和 Windows ICO 位于同目录；Windows、DEB、RPM、AppImage 均使用它。
- 窗口图标由 `src/main_gui.py` 加载；macOS 若由系统管理 bundle 图标，会安全跳过 Tk 图标设置。
- UI 使用浅色/深色模式，样式令牌在 `src/ui_style.py`。

## 功能概览

- 图标生成器、局域网扫描器、本地端口占用管理、二维码生成、图片压缩与格式转换。
- 工具页实现主要在：`src/icon_generator.py`、`src/lan_scanner.py`、`src/utility_pages.py`。
- 核心逻辑包括：`src/port_inspector.py`、`src/qr_generator.py`、`src/image_processor.py`。

## 常用验证

```bash
uv run python -m unittest tests/test_tool_cores.py tests/test_ui_style.py tests/test_main_gui.py tests/test_version.py
bash tests/test_install.sh
bash -n install.sh
uv run python -m compileall -q src utilbox.py scripts
```

对 Linux 发布包变更，优先在 `distrobox` 的 Debian 12 容器中实际构建并启动测试；不要只依赖 GitHub Actions 的构建成功。
