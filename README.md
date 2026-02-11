# 🛠️ 多功能工具箱

一个现代化的多功能小工具集合，支持Windows和Linux。

## ✨ 功能特性

### 🎨 图标生成器
- 现代化GUI界面（深色主题）
- 实时图片预览
- 多尺寸ICO支持（16x16 到 256x256）
- 支持多种图片格式（PNG, JPG, BMP, GIF）
- 全选/清空快捷操作

### 🔍 局域网扫描器
- 自动检测本机IP和网络段
- 快速扫描局域网内活跃主机
- 检测常用端口（22, 80, 81, 7125, 9080, 50051）
- 显示主机名和开放端口
- 实时进度显示

## 🚀 快速开始

### 开发环境运行

```bash
# 安装依赖
uv sync

# 运行主程序（需要X11支持）
uv run python main_gui.py

# 单独测试图标生成器
uv run python icon_generator.py

# 单独测试局域网扫描器
uv run python lan_scanner.py
```

### Windows打包

```bash
# 1. 安装开发依赖
uv sync --extra dev

# 2. 运行打包脚本
uv run python build.py

# 3. 可执行文件位置
# dist/toolbox.exe
```

## 📖 使用说明

### 主界面
启动程序后，在主界面选择需要使用的工具：
- **图标生成器** - 转换图片为ICO格式
- **局域网扫描器** - 扫描局域网设备

### 图标生成器
1. 点击"选择图片文件"按钮
2. 查看图片信息和预览
3. 选择需要的ICO尺寸（可使用全选/清空）
4. 点击"转换为ICO"并选择保存位置

### 局域网扫描器
1. 自动检测本机IP和网络段
2. 可手动修改网络段（如 192.168.1.0/24）
3. 点击"开始扫描"
4. 查看扫描结果（IP、主机名、开放端口）

## 🛠️ 技术栈

- **GUI框架**: CustomTkinter（现代化界面）
- **图片处理**: Pillow（PIL）
- **网络扫描**: socket + concurrent.futures
- **打包工具**: PyInstaller
- **包管理**: uv

## 📁 项目结构

```
png2ico/
├── main_gui.py          # 主界面入口
├── icon_generator.py    # 图标生成器页面
├── lan_scanner.py       # 局域网扫描器页面
├── converter.py         # 图片转换核心逻辑
├── scanner_core.py      # 网络扫描核心逻辑
├── gui.py               # 原独立版图标生成器（已废弃）
├── build.py             # Windows打包脚本
├── tests/               # 测试文件
├── examples/            # 测试图片
├── pyproject.toml       # 项目配置
└── README.md            # 说明文档
```

## 📝 注意事项

- WSL环境需要X11服务器才能运行GUI
- Windows环境可直接运行或打包成exe
- 局域网扫描器默认扫描端口：22(SSH), 80(HTTP), 81(HTTP-Alt), 7125(Moonraker), 9080(Device-API), 50051(Voice-API)
- 扫描速度取决于网络环境和主机数量

## 🐛 问题排查

**WSL中无法显示GUI？**
- 安装WSLg或X11服务器（如VcXsrv）
- 或直接在Windows上运行

**打包失败？**
- 确保已安装开发依赖：`uv sync --extra dev`
- 检查PyInstaller版本是否兼容

**扫描器无法发现设备？**
- 检查防火墙设置
- 确认网络段配置正确
- 某些设备可能禁用了端口响应

## 📄 许可证

MIT License
