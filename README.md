# 🖼️ PNG to ICO Converter

一个现代化的图片转ICO格式工具，支持Windows和Linux。

## ✨ 功能特性

- 🎨 现代化GUI界面（深色主题）
- 📸 实时图片预览
- 📏 多尺寸ICO支持（16x16 到 256x256）
- 🔄 支持多种图片格式（PNG, JPG, BMP, GIF）
- 💻 跨平台（Windows, Linux）

## 🚀 快速开始

### 开发环境运行

```bash
# 安装依赖
uv sync

# 运行程序（需要X11支持）
uv run python gui.py

# 测试核心功能（无需GUI）
uv run python tests/test_converter.py
```

### Windows打包

```bash
# 1. 安装开发依赖
uv sync --extra dev

# 2. 运行打包脚本
uv run python build.py

# 3. 可执行文件位置
# dist/png2ico.exe
```

## 📖 使用说明

1. **选择图片** - 点击"选择图片文件"按钮
2. **预览图片** - 查看图片信息和预览
3. **选择尺寸** - 勾选需要的ICO尺寸
4. **转换保存** - 点击"转换为ICO"并选择保存位置

## 🛠️ 技术栈

- **GUI框架**: CustomTkinter（现代化界面）
- **图片处理**: Pillow（PIL）
- **打包工具**: PyInstaller
- **包管理**: uv

## 📁 项目结构

```
png2ico/
├── gui.py               # GUI界面和程序入口
├── converter.py         # 转换核心逻辑
├── build.py             # Windows打包脚本
├── tests/               # 测试文件
│   └── test_converter.py
├── examples/            # 测试图片
├── pyproject.toml       # 项目配置
└── README.md            # 说明文档
```

## 📝 注意事项

- WSL环境需要X11服务器才能运行GUI
- Windows环境可直接运行或打包成exe
- 打包后的exe约30MB大小
- 支持的输入格式：PNG, JPG, JPEG, BMP, GIF
- ICO标准尺寸：16, 32, 48, 64, 128, 256

## 🐛 问题排查

**WSL中无法显示GUI？**
- 安装WSLg或X11服务器（如VcXsrv）
- 或直接在Windows上运行

**打包失败？**
- 确保已安装开发依赖：`uv sync --extra dev`
- 检查PyInstaller版本是否兼容

## 📄 许可证

MIT License
