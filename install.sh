#!/bin/bash
# UtilBox 安装脚本 - Linux

set -e

echo "=================================="
echo "  UtilBox 安装脚本"
echo "=================================="
echo ""

# 检查是否已安装 uv
if ! command -v uv &> /dev/null; then
    echo "📦 正在安装 uv 包管理器..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # 添加到当前 shell
    export PATH="$HOME/.local/bin:$PATH"

    echo "✅ uv 安装完成"
    echo ""
else
    echo "✅ uv 已安装"
    echo ""
fi

# 检查系统依赖
echo "📋 检查系统依赖..."
if ! dpkg -l | grep -q python3-tk; then
    echo "⚠️  缺少 python3-tk，正在安装..."
    sudo apt update
    sudo apt install -y python3-tk
    echo "✅ python3-tk 安装完成"
else
    echo "✅ python3-tk 已安装"
fi

# 检查中文字体
if ! dpkg -l | grep -q fonts-noto-cjk; then
    echo "⚠️  缺少中文字体，正在安装..."
    sudo apt install -y fonts-noto-cjk
    echo "✅ 中文字体安装完成"
else
    echo "✅ 中文字体已安装"
fi

echo ""
echo "📦 安装 Python 依赖..."
uv sync

echo ""
echo "=================================="
echo "  ✅ 安装完成！"
echo "=================================="
echo ""
echo "运行方式："
echo "  python utilbox.py"
echo ""
echo "或者："
echo "  uv run python utilbox.py"
echo ""
