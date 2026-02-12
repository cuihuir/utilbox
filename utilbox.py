#!/usr/bin/env python3
"""UtilBox - 多功能实用工具箱启动入口"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from main_gui import ToolboxApp


def main():
    """主函数"""
    app = ToolboxApp()
    app.mainloop()


if __name__ == "__main__":
    main()
