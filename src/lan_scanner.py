"""局域网扫描器页面"""
import customtkinter as ctk
import ipaddress
from tkinter import messagebox
import threading
from scanner_core import NetworkScanner
from ui_style import APP_BG, CONTROL_FILL, CONTROL_HOVER, DESTRUCTIVE, INK, INPUT_BG, ON_PRIMARY, PRIMARY, PRIMARY_HOVER, SECONDARY, SUCCESS, SURFACE, ui_font


class LanScannerPage(ctk.CTkFrame):
    """局域网扫描器页面"""

    def __init__(self, parent, back_callback):
        super().__init__(parent, fg_color=APP_BG)

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
        top_bar.pack(fill="x", pady=(6, 8), padx=20)

        # 返回按钮
        back_btn = ctk.CTkButton(
            top_bar,
            text="← 返回",
            command=self.back_callback,
            width=80,
            height=32,
            font=ui_font(13),
            fg_color=CONTROL_FILL,
            hover_color=CONTROL_HOVER,
            text_color=INK
        )
        back_btn.pack(side="left")

        # 标题
        title_label = ctk.CTkLabel(
            top_bar,
            text="局域网扫描器",
            font=ui_font(20, weight="bold"), text_color=INK
        )
        title_label.pack(side="left", padx=20)

        # 配置区域
        config_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        config_frame.pack(pady=(0, 6), padx=20, fill="x")

        # 本机IP
        ip_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        ip_row.pack(pady=(8, 4), padx=15, fill="x")

        ctk.CTkLabel(
            ip_row,
            text="本机IP:",
            font=ui_font(12, weight="bold"), text_color=INK,
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))

        self.local_ip_label = ctk.CTkLabel(
            ip_row,
            text="检测中...",
            font=ui_font(12),
            text_color=PRIMARY
        )
        self.local_ip_label.pack(side="left")

        # 网络段输入
        network_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        network_row.pack(pady=4, padx=15, fill="x")

        ctk.CTkLabel(
            network_row,
            text="网络段:",
            font=ui_font(12, weight="bold"), text_color=INK,
            width=80,
            anchor="w"
        ).pack(side="left", padx=(0, 10))

        self.ip_entries = []
        for index in range(4):
            entry = ctk.CTkEntry(network_row, width=48, justify="center", font=ui_font(12), fg_color=INPUT_BG, border_color=CONTROL_HOVER, text_color=INK)
            entry.pack(side="left")
            self.ip_entries.append(entry)
            if index < 3:
                ctk.CTkLabel(network_row, text=".", font=ui_font(14, "bold"), text_color=SECONDARY, width=10).pack(side="left")
        ctk.CTkLabel(network_row, text="/", font=ui_font(14, "bold"), text_color=SECONDARY, width=16).pack(side="left")
        self.prefix_entry = ctk.CTkEntry(network_row, width=42, justify="center", font=ui_font(12), fg_color=INPUT_BG, border_color=CONTROL_HOVER, text_color=INK)
        self.prefix_entry.pack(side="left", padx=(0, 10))

        # 扫描端口显示
        ctk.CTkLabel(
            network_row,
            text=f"扫描端口: {', '.join(map(str, NetworkScanner.DEFAULT_PORTS.keys()))}",
            font=ui_font(10),
            text_color=SECONDARY
        ).pack(side="left", padx=10)

        # 扫描按钮
        self.scan_btn = ctk.CTkButton(
            config_frame,
            text="开始扫描",
            command=self._start_scan,
            font=ui_font(14, weight="bold"),
            height=36,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER
        )
        self.scan_btn.pack(pady=(6, 8), padx=15, fill="x")

        # 进度条
        progress_row = ctk.CTkFrame(self, fg_color="transparent")
        progress_row.pack(fill="x", padx=20, pady=(0, 4))
        self.progress_bar = ctk.CTkProgressBar(progress_row, mode="determinate", fg_color=CONTROL_FILL, progress_color=PRIMARY)
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)

        # 状态标签
        self.status_label = ctk.CTkLabel(
            progress_row,
            text="就绪",
            font=ui_font(11),
            text_color=SECONDARY
        )
        self.status_label.pack(side="right", padx=(12, 0))

        # 结果区域
        result_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        result_frame.pack(pady=(4, 10), padx=20, fill="both", expand=True)

        result_title = ctk.CTkLabel(
            result_frame,
            text="扫描结果",
            font=ui_font(12, weight="bold"), text_color=INK, anchor="w"
        )
        result_title.pack(fill="x", padx=20, pady=(14, 8))

        self.result_summary = ctk.CTkLabel(result_frame, text="等待开始扫描", font=ui_font(12), text_color=SECONDARY, anchor="w")
        self.result_summary.pack(fill="x", padx=20, pady=(0, 8))
        self.results_list = ctk.CTkScrollableFrame(result_frame, fg_color="transparent")
        self.results_list.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.empty_label = ctk.CTkLabel(self.results_list, text="扫描结果会显示在这里", font=ui_font(13), text_color=SECONDARY)
        self.empty_label.pack(pady=35)

        # 初始化结果计数
        self.found_count = 0

    def _auto_detect_network(self):
        """自动检测网络信息"""
        try:
            local_ip = self.scanner.get_local_ip()
            self.local_ip_label.configure(text=local_ip)

            self._set_network(self.scanner.get_network_range(local_ip))
        except Exception as e:
            self.local_ip_label.configure(text="检测失败")
            messagebox.showerror("错误", f"网络检测失败: {str(e)}")

    def _start_scan(self):
        """开始扫描"""
        if self.is_scanning:
            # 停止扫描
            self.scanner.stop_scan()
            self.is_scanning = False
            self.scan_btn.configure(text="开始扫描", fg_color=PRIMARY)
            self.status_label.configure(text="已停止")
            return

        try:
            network = self._network_value()
        except ValueError as error:
            messagebox.showwarning("网络段无效", str(error))
            return

        # 清空结果
        self._clear_results()
        self.progress_bar.set(0)
        self.found_count = 0

        # 更新UI状态
        self.is_scanning = True
        self.scan_btn.configure(text="停止扫描", fg_color=DESTRUCTIVE)
        self.status_label.configure(text="扫描中...")
        self.result_summary.configure(text="正在扫描局域网…")

        # 在新线程中执行扫描
        thread = threading.Thread(target=self._scan_thread, args=(network,), daemon=True)
        thread.start()

    def _set_network(self, network):
        parsed = ipaddress.IPv4Network(network, strict=False)
        for entry, octet in zip(self.ip_entries, str(parsed.network_address).split(".")):
            entry.delete(0, "end")
            entry.insert(0, octet)
        self.prefix_entry.delete(0, "end")
        self.prefix_entry.insert(0, str(parsed.prefixlen))

    def _network_value(self):
        values = [entry.get().strip() for entry in self.ip_entries]
        if any(not value for value in values):
            raise ValueError("请填写完整的 IPv4 地址")
        try:
            octets = [int(value) for value in values]
            if any(value < 0 or value > 255 for value in octets):
                raise ValueError
            prefix = int(self.prefix_entry.get().strip())
            if not 0 <= prefix <= 32:
                raise ValueError
        except ValueError as error:
            raise ValueError("IPv4 地址或前缀长度无效") from error
        return str(ipaddress.IPv4Network(f"{'.'.join(map(str, octets))}/{prefix}", strict=False))

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

        if self.empty_label.winfo_exists(): self.empty_label.destroy()
        row = ctk.CTkFrame(self.results_list, fg_color=CONTROL_FILL, corner_radius=10)
        row.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(row, text="●", text_color=SUCCESS, font=ui_font(14)).pack(side="left", padx=(12, 8), pady=10)
        details = ctk.CTkFrame(row, fg_color="transparent")
        details.pack(side="left", fill="x", expand=True, pady=8)
        ctk.CTkLabel(details, text=host['ip'], text_color=INK, font=ui_font(14, "bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(details, text=host['hostname'], text_color=SECONDARY, font=ui_font(12), anchor="w").pack(fill="x")
        ports = [f"{port} · {self.scanner.get_service_name(port)}" for port, open_ in host['ports'].items() if open_]
        ctk.CTkLabel(row, text="\n".join(ports), text_color=PRIMARY, font=ui_font(11), justify="right").pack(side="right", padx=12)
        self.result_summary.configure(text=f"已发现 {self.found_count} 台设备")

    def _show_summary(self, results):
        """显示扫描统计信息"""
        if self.found_count == 0:
            self.empty_label = ctk.CTkLabel(self.results_list, text="未发现活跃设备\n请检查网络段或稍后重试", font=ui_font(13), text_color=SECONDARY, justify="center")
            self.empty_label.pack(pady=35)
            self.result_summary.configure(text="扫描完成，未发现活跃设备")
        else:
            self.result_summary.configure(text=f"扫描完成，发现 {self.found_count} 台活跃设备")

    def _scan_finished(self):
        """扫描完成"""
        self.is_scanning = False
        self.scan_btn.configure(text="开始扫描", fg_color=PRIMARY)
        self.status_label.configure(text="扫描完成")
        self.progress_bar.set(1.0)

    def _clear_results(self):
        for child in self.results_list.winfo_children(): child.destroy()
        self.empty_label = ctk.CTkLabel(self.results_list, text="正在准备扫描…", font=ui_font(13), text_color=SECONDARY)
        self.empty_label.pack(pady=35)


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
