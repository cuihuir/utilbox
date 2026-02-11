"""测试扫描器核心功能（无需GUI）"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner_core import NetworkScanner


def test_scanner():
    """测试扫描器功能"""
    scanner = NetworkScanner()

    print("=" * 60)
    print("局域网扫描器测试")
    print("=" * 60)

    # 测试1: 获取本机IP
    print("\n1. 获取本机IP")
    local_ip = scanner.get_local_ip()
    print(f"   本机IP: {local_ip}")

    # 测试2: 获取网络段
    print("\n2. 获取网络段")
    network = scanner.get_network_range(local_ip)
    print(f"   网络段: {network}")

    # 测试3: 检测本机端口
    print("\n3. 检测本机端口")
    print(f"   扫描端口: {list(NetworkScanner.DEFAULT_PORTS.keys())}")
    result = scanner.check_host(local_ip, list(NetworkScanner.DEFAULT_PORTS.keys()))
    print(f"   主机名: {result['hostname']}")
    print(f"   在线状态: {result['alive']}")
    print(f"   开放端口:")
    for port, is_open in result['ports'].items():
        status = "✓ 开放" if is_open else "✗ 关闭"
        service = NetworkScanner.get_service_name(port)
        print(f"      {port:5d} ({service:15s}) - {status}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print("\n提示: 要扫描整个网络，请运行 GUI 程序:")
    print("  uv run python main_gui.py")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_scanner()
