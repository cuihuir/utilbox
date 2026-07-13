"""图标生成器页面"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from converter import ImageConverter
from ui_style import APP_BG, CONTROL_FILL, CONTROL_HOVER, INK, INPUT_BG, ON_PRIMARY, PRIMARY, PRIMARY_HOVER, SECONDARY, SURFACE, ui_font


class IconGeneratorPage(ctk.CTkFrame):
    """图标生成器页面（作为Frame嵌入主窗口）"""

    def __init__(self, parent, back_callback):
        super().__init__(parent, fg_color=APP_BG)

        # 初始化转换器
        self.converter = ImageConverter()
        self.current_image_path = None
        self.preview_image = None
        self.back_callback = back_callback

        # 创建界面
        self._create_widgets()

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
            font=ui_font(13),
            fg_color=CONTROL_FILL,
            hover_color=CONTROL_HOVER,
            text_color=INK
        )
        back_btn.pack(side="left")

        # 标题
        title_label = ctk.CTkLabel(
            top_bar,
            text="图标生成器",
            font=ui_font(20, weight="bold"), text_color=INK
        )
        title_label.pack(side="left", padx=20)

        # 选择图片按钮
        self.select_btn = ctk.CTkButton(
            self,
            text="选择图片文件",
            command=self._select_file,
            font=ui_font(14, weight="bold"),
            height=50,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=ON_PRIMARY
        )
        self.select_btn.pack(pady=10, padx=20, fill="x")

        # 图片预览区域
        preview_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        preview_frame.pack(pady=8, padx=20, fill="x")

        preview_title = ctk.CTkLabel(
            preview_frame,
            text="图片预览",
            font=ui_font(12, weight="bold"),
            text_color=INK
        )
        preview_title.pack(pady=6)

        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="",
            font=ui_font(12),
            width=150,
            height=150
        )
        self.preview_label.pack(pady=6)

        self.info_label = ctk.CTkLabel(
            preview_frame,
            text="",
            font=ui_font(10),
            text_color=SECONDARY
        )
        self.info_label.pack(pady=4)

        # ICO尺寸选择区域
        size_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        size_frame.pack(pady=8, padx=20, fill="x")

        # 标题栏带快捷操作
        title_bar = ctk.CTkFrame(size_frame, fg_color="transparent")
        title_bar.pack(pady=8, padx=20, fill="x")

        size_title = ctk.CTkLabel(
            title_bar,
            text="ICO尺寸选择",
            font=ui_font(12, weight="bold"),
            text_color=INK
        )
        size_title.pack(side="left")

        # 快捷操作按钮
        quick_actions = ctk.CTkFrame(title_bar, fg_color="transparent")
        quick_actions.pack(side="right")

        select_all_btn = ctk.CTkButton(
            quick_actions,
            text="全选",
            command=self._select_all_sizes,
            width=60,
            height=24,
            font=ui_font(10),
            fg_color=CONTROL_FILL,
            hover_color=CONTROL_HOVER,
            text_color=PRIMARY
        )
        select_all_btn.pack(side="left", padx=4)

        clear_all_btn = ctk.CTkButton(
            quick_actions,
            text="清空",
            command=self._clear_all_sizes,
            width=60,
            height=24,
            font=ui_font(10),
            fg_color=CONTROL_FILL,
            hover_color=CONTROL_HOVER,
            text_color=INK
        )
        clear_all_btn.pack(side="left", padx=4)

        # 创建复选框 - 使用更明显的样式
        self.size_vars = {}

        sizes = [16, 32, 48, 64, 128, 256]

        # 第一行：16x16, 32x32, 48x48
        row1_frame = ctk.CTkFrame(size_frame, fg_color="transparent")
        row1_frame.pack(pady=4, padx=20)

        for size in sizes[:3]:
            var = ctk.BooleanVar(value=True)
            self.size_vars[size] = var

            checkbox = ctk.CTkCheckBox(
                row1_frame,
                text=f"  {size}x{size}  ",
                variable=var,
                font=ui_font(12, weight="bold"),
                checkbox_width=22,
                checkbox_height=22,
                border_width=2,
                corner_radius=4,
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER,
                border_color=PRIMARY,
                text_color=INK,
                checkmark_color=ON_PRIMARY
            )
            checkbox.pack(side="left", padx=20, pady=6)

        # 第二行：64x64, 128x128, 256x256
        row2_frame = ctk.CTkFrame(size_frame, fg_color="transparent")
        row2_frame.pack(pady=4, padx=20, fill="x")

        for size in sizes[3:]:
            var = ctk.BooleanVar(value=True)
            self.size_vars[size] = var

            checkbox = ctk.CTkCheckBox(
                row2_frame,
                text=f"  {size}x{size}  ",
                variable=var,
                font=ui_font(12, weight="bold"),
                checkbox_width=22,
                checkbox_height=22,
                border_width=2,
                corner_radius=4,
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER,
                border_color=PRIMARY,
                text_color=INK,
                checkmark_color=ON_PRIMARY
            )
            checkbox.pack(side="left", padx=20, pady=6)

        # 添加底部间距
        ctk.CTkLabel(size_frame, text="", font=ui_font(12), height=6).pack()

        # 转换按钮（移到底部）
        self.convert_btn = ctk.CTkButton(
            self,
            text="转换为 ICO",
            command=self._convert_image,
            font=ui_font(14, weight="bold"),
            height=50,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=ON_PRIMARY,
            state="disabled"
        )
        self.convert_btn.pack(pady=10, padx=20, fill="x")

        # 状态栏
        status_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14)
        status_frame.pack(pady=8, padx=20, fill="x")

        self.file_label = ctk.CTkLabel(
            status_frame,
            text="文件: 未选择",
            font=ui_font(11),
            text_color=SECONDARY,
            anchor="w"
        )
        self.file_label.pack(side="left", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="状态: 就绪",
            font=ui_font(11),
            text_color=SECONDARY,
            anchor="e"
        )
        self.status_label.pack(side="right", padx=10, pady=5)

    def _select_file(self):
        """选择图片文件"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("PNG文件", "*.png"),
            ("JPEG文件", "*.jpg *.jpeg"),
            ("所有文件", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=filetypes
        )

        if filename:
            self._load_image(filename)

    def _load_image(self, image_path: str):
        """加载并预览图片"""
        try:
            # 验证图片
            if not self.converter.validate_image(image_path):
                messagebox.showerror("错误", self.converter.last_error)
                return

            self.current_image_path = image_path
            path = Path(image_path)

            # 更新文件标签
            self.file_label.configure(text=f"文件: {path.name}")

            # 加载图片用于预览
            img = Image.open(image_path)

            # 获取图片信息
            info = self.converter.get_image_info(image_path)
            info_text = f"{info['width']}x{info['height']} | {info['format']} | {info['size_kb']:.1f} KB"
            self.info_label.configure(text=info_text)

            # 创建缩略图（保持宽高比）
            img.thumbnail((140, 140), Image.LANCZOS)

            # 转换为PhotoImage
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_image, text="")

            # 启用转换按钮
            self.convert_btn.configure(state="normal")

            # 更新状态
            self.status_label.configure(text="状态: 已加载图片，可以转换")

        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")

    def _select_all_sizes(self):
        """全选所有尺寸"""
        for var in self.size_vars.values():
            var.set(True)

    def _clear_all_sizes(self):
        """清空所有尺寸选择"""
        for var in self.size_vars.values():
            var.set(False)

    def _convert_image(self):
        """转换图片为ICO"""
        if not self.current_image_path:
            messagebox.showwarning("警告", "请先选择图片文件")
            return

        # 获取选中的尺寸
        selected_sizes = [
            size for size, var in self.size_vars.items()
            if var.get()
        ]

        if not selected_sizes:
            messagebox.showwarning("警告", "请至少选择一个ICO尺寸")
            return

        # 选择保存位置
        default_name = Path(self.current_image_path).stem + ".ico"
        output_path = filedialog.asksaveasfilename(
            title="保存ICO文件",
            defaultextension=".ico",
            initialfile=default_name,
            filetypes=[("ICO文件", "*.ico"), ("所有文件", "*.*")]
        )

        if not output_path:
            return

        # 更新状态
        self.status_label.configure(text="状态: 转换中...")
        self.update()

        # 执行转换
        success, message = self.converter.convert_to_ico(
            self.current_image_path,
            output_path,
            selected_sizes
        )

        if success:
            self.status_label.configure(text=f"状态: {message}")
            messagebox.showinfo("成功", f"{message}\n\n保存位置:\n{output_path}")
        else:
            self.status_label.configure(text="状态: 转换失败")
            messagebox.showerror("错误", message)


# 如果直接运行此文件，创建独立窗口用于测试
if __name__ == "__main__":
    class TestApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("图标生成器 - 测试")
            self.geometry("650x750")
            ctk.set_appearance_mode("dark")

            page = IconGeneratorPage(self, self.quit)
            page.pack(fill="both", expand=True)

    app = TestApp()
    app.mainloop()
