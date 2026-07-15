import psutil
import subprocess


class PortInspector:
    """List local listening sockets and their owning processes."""

    def listening_ports(self):
        entries = []
        for connection in psutil.net_connections(kind="inet"):
            if connection.status != psutil.CONN_LISTEN or not connection.laddr:
                continue
            process_name = "未知"
            if connection.pid:
                try:
                    process_name = psutil.Process(connection.pid).name()
                except (psutil.Error, OSError):
                    pass
            entries.append({"address": connection.laddr.ip, "port": connection.laddr.port, "pid": connection.pid, "process": process_name})
        return sorted(entries, key=lambda item: item["port"])

    def terminate(self, pid: int, use_system_authorization: bool = False):
        if not pid:
            raise ValueError("该端口没有可终止的进程")
        if use_system_authorization:
            result = subprocess.run(["pkexec", "kill", "-TERM", str(pid)], capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or "系统未允许终止进程")
            return
        try:
            psutil.Process(pid).terminate()
        except psutil.AccessDenied as error:
            raise PermissionError("需要系统授权") from error
