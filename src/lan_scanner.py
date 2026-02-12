"""局域网扫描器页面"""
import customtkinter as ctk
from tkinter import messagebox
import threading
from scanner_core import NetworkScanner


class LanScannerPage(ctk.CTkFrame):
    """局域网扫描器页面"""

    def __init__(self, parent, back_callback):
        super().__init__(parent, fg_color="transparent")

        self.scanner = NetworkScanner()
        self.back_callback = back_callback
        self.is_scanning = False

        # 创建界面
        self._create_widgets()

        # 自动检测本机IP和网络段
        self._auto_detect_network()

    def _create_widgets(self):
        """创建所有界面组件"""

        # 顶部栏：返回按钮 + 标题
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", pady=(10, 15), padx=20)

        # 返回按钮
        back_btn = ctk.CTkButton(
            top_bar,
            text="← 返回",
            command=self.back_callback,
            width=80,
            height=32,
            font=ctk.CTkFont(size=13),
            fg_color="#444444",
            hover_color="#555555"
        )
        back_btn.pack(side="left")

        # 标题
        title_label = ctk.CTkLabel(
            top_bar,
            text="🔍 局域网扫描器",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=20)

        # 配置区域
        config_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        config_frame.pack(pady=10, padx=20, fill="x")

        # 本机IP
        ip_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        ip_row.pack(pady=8, padx=15, fill="x")

        ctk.CTkLabel(
            ip_row,
            text="本机IP:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))

        self.local_ip_label = ctk.CTkLabel(
            ip_row,
            text="检测中...",
            font=ctk.CTkFont(size=12),
            text_color="#5B8DEE"
        )
        self.local_ip_label.pack(side="left")

        # 网络段输入
        network_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        network_row.pack(pady=8, padx=15, fill="x")

        ctk.CTkLabel(
            network_row,
            text="网络段:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))

        self.network_entry = ctk.CTkEntry(
            network_row,
            placeholder_text="例如: 192.168.1.0/24",
            font=ctk.CTkFont(size=12),
            width=200
        )
        self.network_entry.pack(side="left", padx=(0, 10))

        # 扫描端口显示
        ctk.CTkLabel(
            network_row,
            text=f"扫描端口: {', '.join(map(str, NetworkScanner.DEFAULT_PORTS.keys()))}",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        ).pack(side="left", padx=10)

        # 扫描按钮
        self.scan_btn = ctk.CTkButton(
            config_frame,
            text="🔍 开始扫描",
            command=self._start_scan,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        self.scan_btn.pack(pady=10, padx=15, fill="x")

        # 进度条
        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
        self.progress_bar.pack(pady=5, padx=20, fill="x")
        self.progress_bar.set(0)

        # 状态标签
        self.status_label = ctk.CTkLabel(
            self,
            text="就绪",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        self.status_label.pack(pady=5)

        # 结果区域
        result_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        result_title = ctk.CTkLabel(
            result_frame,
            text="扫描结果",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        result_title.pack(pady=8)

        # 结果文本框（使用CTkTextbox）
        self.result_text = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(family="Courier New", size=13),
            wrap="none"
        )
        self.result_text.pack(pady=5, padx=10, fill="both", expand=True)

        # 初始化结果计数
        self.found_count = 0

    def _auto_detect_network(self):
        """自动检测网络信息"""
        try:
            local_ip = self.scanner.get_local_ip()
            self.local_ip_label.configure(text=local_ip)

            network = self.scanner.get_network_range(local_ip)
            self.network_entry.delete(0, "end")
            self.network_entry.insert(0, network)
        except Exception as e:
            self.local_ip_label.configure(text="检测失败")
            messagebox.showerror("错误", f"网络检测失败: {str(e)}")

    def _start_scan(self):
        """开始扫描"""
        if self.is_scanning:
            # 停止扫描
            self.scanner.stop_scan()
            self.is_scanning = False
            self.scan_btn.configure(text="🔍 开始扫描", fg_color="#2ECC71")
            self.status_label.configure(text="已停止")
            return

        network = self.network_entry.get().strip()
        if not network:
            messagebox.showwarning("警告", "请输入网络段")
            return

        # 清空结果
        self.result_text.delete("1.0", "end")
        self.progress_bar.set(0)
        self.found_count = 0

        # 显示表头
        header = f"{'IP地址':<15} {'主机名':<20} {'开放端口'}\n"
        separator = "=" * 80 + "\n"
        self.result_text.insert("end", header)
        self.result_text.insert("end", separator)

        # 更新UI状态
        self.is_scanning = True
        self.scan_btn.configure(text="⏸ 停止扫描", fg_color="#E74C3C")
        self.status_label.configure(text="扫描中...")

        # 在新线程中执行扫描
        thread = threading.Thread(target=self._scan_thread, args=(network,), daemon=True)
        thread.start()

    def _scan_thread(self, network: str):
        """扫描线程"""
        try:
            def progress_callback(current, total, message, host_result=None):
                # 更新进度条和状态
                if total > 0:
                    progress = current / total
                    self.after(0, lambda: self.progress_bar.set(progress))
                self.after(0, lambda: self.status_label.configure(text=message))

                # 如果发现活跃主机，实时显示
                if host_result:
                    self.after(0, lambda: self._add_host_to_results(host_result))

            # 执行扫描
            results = self.scanner.scan_network(
                network,
                progress_callback=progress_callback,
                max_workers=50
            )

            # 显示统计信息
            self.after(0, lambda: self._show_summary(results))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"扫描失败: {str(e)}"))
        finally:
            self.after(0, self._scan_finished)

    def _add_host_to_results(self, host):
        """实时添加发现的主机到结果"""
        self.found_count += 1

        ip = host['ip']
        hostname = host['hostname']
        open_ports = [
            f"{port}({self.scanner.get_service_name(port)})"
            for port, is_open in host['ports'].items()
            if is_open
        ]
        ports_str = ', '.join(open_ports)

        line = f"{ip:<15} {hostname:<20} {ports_str}\n"
        self.result_text.insert("end", line)

        # 自动滚动到底部
        self.result_text.see("end")

    def _show_summary(self, results):
        """显示扫描统计信息"""
        separator = "=" * 80 + "\n"
        self.result_text.insert("end", separator)

        if self.found_count == 0:
            self.result_text.insert("end", "\n未发现活跃主机\n")
        else:
            self.result_text.insert("end", f"\n扫描完成！共发现 {self.found_count} 台活跃主机\n")

        # 自动滚动到底部
        self.result_text.see("end")

    def _scan_finished(self):
        """扫描完成"""
        self.is_scanning = False
        self.scan_btn.configure(text="🔍 开始扫描", fg_color="#2ECC71")
        self.status_label.configure(text="扫描完成")
        self.progress_bar.set(1.0)


# 如果直接运行此文件，创建独立窗口用于测试
if __name__ == "__main__":
    class TestApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("局域网扫描器 - 测试")
            self.geometry("800x700")
            ctk.set_appearance_mode("dark")

            page = LanScannerPage(self, self.quit)
            page.pack(fill="both", expand=True)

    app = TestApp()
    app.mainloop()
