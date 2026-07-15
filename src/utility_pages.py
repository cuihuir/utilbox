import customtkinter as ctk
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from image_processor import ImageProcessor
from port_inspector import PortInspector
from qr_generator import QrGenerator
from ui_style import APP_BG, CONTROL_FILL, CONTROL_HOVER, HOVER_SURFACE, INK, ON_PRIMARY, PRIMARY, PRIMARY_HOVER, SECONDARY, SURFACE, ui_font


class ToolPage(ctk.CTkFrame):
    def __init__(self, parent, title, back_callback):
        super().__init__(parent, fg_color=APP_BG)
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=12)
        ctk.CTkButton(bar, text="← 返回", width=80, command=back_callback, fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(13)).pack(side="left")
        ctk.CTkLabel(bar, text=title, font=ui_font(20, "bold"), text_color=INK).pack(side="left", padx=20)


class PortInspectorPage(ToolPage):
    def __init__(self, parent, back_callback):
        super().__init__(parent, "本地端口占用", back_callback)
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=(0, 10))
        self.search = ctk.CTkEntry(controls, placeholder_text="搜索端口号", width=160, fg_color=SURFACE, text_color=INK, font=ui_font(13))
        self.search.pack(side="left")
        self.search._entry.bind("<Return>", lambda _event: self.render())
        self.search._entry.bind("<KP_Enter>", lambda _event: self.render())
        ctk.CTkButton(controls, text="搜索", width=70, command=self.render, fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(13)).pack(side="left", padx=8)
        ctk.CTkButton(controls, text="刷新", width=70, command=self.refresh, fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(13)).pack(side="left")
        self.status = ctk.CTkLabel(controls, text="等待读取", text_color=SECONDARY, font=ui_font(12))
        self.status.pack(side="right")
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=SURFACE, corner_radius=14)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.entries = []
        self.selected_key = None
        self.rows = {}
        ctk.CTkLabel(self.list_frame, text="正在读取本地监听端口…", text_color=SECONDARY, font=ui_font(14)).pack(pady=30)
        self.after(150, self.refresh)
    def refresh(self):
        self.status.configure(text="正在刷新…")
        threading.Thread(target=self._load_ports, daemon=True).start()
    def _load_ports(self):
        entries = PortInspector().listening_ports()
        self.after(0, lambda: self._loaded(entries))
    def _loaded(self, entries):
        self.entries = entries
        self.status.configure(text=f"{len(entries)} 个监听端口")
        self.render()
    def render(self):
        for child in self.list_frame.winfo_children(): child.destroy()
        self.rows = {}
        query = self.search.get().strip()
        matching = 0
        for item in self.entries:
            if query and query not in str(item["port"]): continue
            matching += 1
            key = (item["address"], item["port"], item["pid"])
            selected = key == self.selected_key
            row = ctk.CTkFrame(self.list_frame, fg_color=HOVER_SURFACE if selected else "transparent", corner_radius=8)
            row.pack(fill="x", padx=8, pady=4)
            label = ctk.CTkLabel(row, text=f"{item['process']}  ·  {item['address']}:{item['port']}  ·  PID {item['pid'] or '-'}", text_color=INK, font=ui_font(13), anchor="w")
            label.pack(side="left", fill="x", expand=True, padx=8, pady=8)
            close = ctk.CTkButton(row, text="关闭", width=64, command=lambda entry=item: self.terminate(entry), fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(12))
            close.pack(side="right", padx=6, pady=4)
            for widget in (row, label):
                widget.bind("<Button-1>", lambda _event, entry=item: self.select(entry))
            self.rows[key] = row
        if matching == 0:
            ctk.CTkLabel(self.list_frame, text="没有匹配的监听端口", text_color=SECONDARY, font=ui_font(14)).pack(pady=30)
    def select(self, entry):
        self.selected_key = (entry["address"], entry["port"], entry["pid"])
        for key, row in self.rows.items():
            row.configure(fg_color=HOVER_SURFACE if key == self.selected_key else "transparent")
    def terminate(self, entry):
        try:
            pid = entry["pid"]
            if not messagebox.askyesno("确认关闭", f"确定要终止 {entry['process']}（PID {pid}）吗？\n关闭后该端口会停止监听。"):
                return
            inspector = PortInspector()
            try:
                inspector.terminate(pid)
            except PermissionError:
                inspector.terminate(pid, use_system_authorization=True)
            self.refresh()
            messagebox.showinfo("已关闭", f"已请求终止 {entry['process']}（PID {pid}）")
        except ValueError:
            messagebox.showwarning("无法终止", "该端口没有可终止的进程")
        except RuntimeError as error:
            messagebox.showerror("无法终止", str(error))


class QrPage(ToolPage):
    def __init__(self, parent, back_callback):
        super().__init__(parent, "二维码工具", back_callback)
        ctk.CTkLabel(self, text="输入文本或链接", font=ui_font(13), text_color=SECONDARY).pack(anchor="w", padx=20, pady=(12, 6))
        self.content = ctk.CTkTextbox(self, height=180, fg_color=SURFACE, text_color=INK, font=ui_font(14))
        self.content.pack(fill="x", padx=20)
        self.preview = ctk.CTkLabel(self, text="生成后将在这里预览", text_color=SECONDARY, font=ui_font(13), width=220, height=220, fg_color=SURFACE, corner_radius=14)
        self.preview.pack(pady=18)
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkButton(actions, text="生成二维码", command=self.generate, fg_color=PRIMARY, hover_color=PRIMARY_HOVER, text_color=ON_PRIMARY, font=ui_font(14, "bold")).pack(side="left", fill="x", expand=True)
        self.save_button = ctk.CTkButton(actions, text="保存 PNG", command=self.save, state="disabled", fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(14, "bold"))
        self.save_button.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self.qr_image = None
    def generate(self):
        try:
            image = QrGenerator().build(self.content.get("1.0", "end"), size=8).convert("RGBA")
            image.thumbnail((190, 190), Image.LANCZOS)
            self.qr_image = ImageTk.PhotoImage(image)
            self.preview.configure(image=self.qr_image, text="")
            self.save_button.configure(state="normal")
        except ValueError as error: messagebox.showwarning("无法生成", str(error))
    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path and self.qr_image:
            QrGenerator().generate(self.content.get("1.0", "end"), path, size=8)
            messagebox.showinfo("完成", f"已保存到:\n{path}")


class ImageProcessorPage(ToolPage):
    def __init__(self, parent, back_callback):
        super().__init__(parent, "图片压缩与转换", back_callback)
        self.files = []
        self.output_dir = None
        self.label = ctk.CTkLabel(self, text="尚未选择图片", font=ui_font(14), text_color=SECONDARY)
        self.label.pack(pady=(30, 12))
        ctk.CTkButton(self, text="选择图片", command=self.choose, fg_color=PRIMARY, hover_color=PRIMARY_HOVER, text_color=ON_PRIMARY, font=ui_font(14, "bold")).pack(fill="x", padx=20)
        settings = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        settings.pack(fill="x", padx=20, pady=20)
        self.format = ctk.CTkOptionMenu(settings, values=["JPEG", "PNG", "WEBP"], font=ui_font(13))
        self.format.pack(side="left", padx=14, pady=14)
        self.quality = ctk.CTkSlider(settings, from_=20, to=100, number_of_steps=16)
        self.quality.set(75); self.quality.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(settings, text="输出目录", command=self.choose_output, width=90, fg_color=CONTROL_FILL, hover_color=CONTROL_HOVER, text_color=INK, font=ui_font(13)).pack(side="right", padx=14)
        ctk.CTkButton(self, text="开始批量处理", command=self.process, fg_color=PRIMARY, hover_color=PRIMARY_HOVER, text_color=ON_PRIMARY, font=ui_font(14, "bold")).pack(fill="x", padx=20)
    def choose(self):
        self.files = filedialog.askopenfilenames(filetypes=[("图片", "*.png *.jpg *.jpeg *.webp *.bmp")])
        self.label.configure(text=f"已选择 {len(self.files)} 张图片")
    def choose_output(self):
        selected = filedialog.askdirectory()
        if selected: self.output_dir = selected
    def process(self):
        if not self.files: return messagebox.showwarning("尚未选择", "请先选择图片")
        if not self.output_dir: return messagebox.showwarning("尚未选择", "请选择输出目录")
        try:
            results = ImageProcessor().process_many(self.files, self.output_dir, self.format.get(), int(self.quality.get()))
            before, after = sum(item["before"] for item in results), sum(item["after"] for item in results)
            messagebox.showinfo("完成", f"已处理 {len(results)} 张图片\n{before / 1024:.1f} KB → {after / 1024:.1f} KB")
        except Exception as error: messagebox.showerror("处理失败", str(error))
