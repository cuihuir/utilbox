"""局域网扫描核心逻辑"""
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Optional


class NetworkScanner:
    """网络扫描器"""

    # 默认扫描的端口及其服务名
    DEFAULT_PORTS = {
        22: "SSH",
        80: "HTTP",
        81: "HTTP-Alt",
        7125: "Moonraker",
        9080: "Device-API",
        50051: "Voice-API"
    }

    def __init__(self):
        self.is_scanning = False

    def get_local_ip(self) -> str:
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"

    def get_network_range(self, ip: str) -> str:
        """根据IP获取网络段（/24）"""
        try:
            network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
            return str(network)
        except Exception:
            return "192.168.1.0/24"

    def check_port(self, ip: str, port: int, timeout: float = 0.5) -> bool:
        """检测单个端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_host(self, ip: str, ports: List[int]) -> Dict:
        """
        检查主机是否在线及端口状态

        Returns:
            {
                'ip': str,
                'hostname': str,
                'alive': bool,
                'ports': {port: bool, ...}
            }
        """
        result = {
            'ip': ip,
            'hostname': 'Unknown',
            'alive': False,
            'ports': {}
        }

        # 检查所有端口
        for port in ports:
            is_open = self.check_port(ip, port)
            result['ports'][port] = is_open
            if is_open:
                result['alive'] = True

        # 如果主机在线，尝试获取主机名
        if result['alive']:
            try:
                result['hostname'] = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                result['hostname'] = 'Unknown'

        return result

    def scan_network(
        self,
        network: str,
        ports: Optional[List[int]] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        max_workers: int = 50
    ) -> List[Dict]:
        """
        扫描网络段内的活跃主机

        Args:
            network: 网络段，如 "192.168.1.0/24"
            ports: 要扫描的端口列表，默认使用DEFAULT_PORTS
            progress_callback: 进度回调函数 (current, total, message)
            max_workers: 最大并发数

        Returns:
            活跃主机列表
        """
        self.is_scanning = True
        active_hosts = []

        if ports is None:
            ports = list(self.DEFAULT_PORTS.keys())

        try:
            net = ipaddress.IPv4Network(network, strict=False)
            hosts = list(net.hosts())
            total = len(hosts)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_ip = {
                    executor.submit(self.check_host, str(ip), ports): str(ip)
                    for ip in hosts
                }

                for i, future in enumerate(as_completed(future_to_ip), 1):
                    if not self.is_scanning:
                        break

                    ip = future_to_ip[future]
                    try:
                        result = future.result()
                        if result['alive']:
                            active_hosts.append(result)
                            if progress_callback:
                                open_ports = [p for p, is_open in result['ports'].items() if is_open]
                                ports_str = ', '.join([f"{p}({self.DEFAULT_PORTS.get(p, 'Unknown')})" for p in open_ports])
                                progress_callback(i, total, f"发现: {ip} - {ports_str}")
                        else:
                            if progress_callback:
                                progress_callback(i, total, f"扫描: {ip}")
                    except Exception as e:
                        if progress_callback:
                            progress_callback(i, total, f"错误: {ip} - {str(e)}")

            # 按IP地址排序
            active_hosts.sort(key=lambda x: ipaddress.IPv4Address(x['ip']))
            return active_hosts

        except Exception as e:
            if progress_callback:
                progress_callback(0, 0, f"扫描错误: {str(e)}")
            return []
        finally:
            self.is_scanning = False

    def stop_scan(self):
        """停止扫描"""
        self.is_scanning = False

    @staticmethod
    def get_service_name(port: int) -> str:
        """获取端口对应的服务名"""
        return NetworkScanner.DEFAULT_PORTS.get(port, "Unknown")
