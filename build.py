"""
Windows打包脚本
使用PyInstaller将应用打包成exe

使用方法:
1. 在Windows环境中安装依赖: uv sync --extra dev
2. 运行此脚本: uv run python build.py
3. 打包后的exe在 dist/toolbox.exe
"""
import PyInstaller.__main__
import shutil
from pathlib import Path


def build_exe():
    """打包为Windows exe"""

    print("=" * 60)
    print("开始打包 多功能工具箱")
    print("=" * 60)

    # 清理旧的构建文件
    for folder in ['build', 'dist']:
        if Path(folder).exists():
            print(f"清理旧文件: {folder}/")
            shutil.rmtree(folder)

    # PyInstaller参数
    args = [
        'main_gui.py',                      # 主程序入口
        '--name=toolbox',                   # 程序名称
        '--onefile',                        # 打包成单个exe
        '--windowed',                       # 无控制台窗口
        '--icon=NONE',                      # 图标（可选）
        '--clean',                          # 清理临时文件
        '--noconfirm',                      # 不询问确认
        # 隐式导入的模块
        '--hidden-import=icon_generator',
        '--hidden-import=lan_scanner',
        '--hidden-import=converter',
        '--hidden-import=scanner_core',
    ]

    print("\n打包参数:")
    for arg in args:
        print(f"  {arg}")

    print("\n开始打包...")
    PyInstaller.__main__.run(args)

    print("\n" + "=" * 60)
    print("✅ 打包完成！")
    print("=" * 60)
    print(f"\n可执行文件位置: {Path('dist/toolbox.exe').absolute()}")
    print("\n使用说明:")
    print("1. 双击 toolbox.exe 运行程序")
    print("2. 在主界面选择需要的工具")
    print("   - 图标生成器: 转换图片为ICO格式")
    print("   - 局域网扫描器: 扫描局域网设备")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    build_exe()
