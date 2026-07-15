"""UtilBox main application window."""
import customtkinter as ctk
from PIL import Image, ImageTk

from icon_generator import IconGeneratorPage
from lan_scanner import LanScannerPage
from utility_pages import ImageProcessorPage, PortInspectorPage, QrPage
from ui_style import APP_BG, CHEVRON, HEADER_BG, HOVER_SURFACE, INK, MAX_CONTENT_WIDTH, PAGE_MARGIN, PRIMARY, ROW_INSET, SECONDARY, SECTION_INSET, SEPARATOR, SUCCESS, SURFACE, icon_path, load_icon, ui_font
from version import __version__


class ToolboxApp(ctk.CTk):
    """Desktop-style launcher for the available local tools."""

    def __init__(self):
        super().__init__()
        self._app_icon = None
        try:
            with Image.open(icon_path("utilbox")) as image:
                self._app_icon = ImageTk.PhotoImage(image.convert("RGBA"))
            self.iconphoto(True, self._app_icon)
        except ctk.TclError:
            # Tk on some desktop platforms manages the bundle icon itself.
            self._app_icon = None
        self.title("工具箱")
        self.geometry("800x600")
        self.minsize(700, 540)
        self.appearance_mode = "light"
        ctk.set_appearance_mode(self.appearance_mode)
        self.configure(fg_color=APP_BG)
        self.current_page = None
        self.home_page = None
        self.icon_page = None
        self.scanner_page = None
        self.port_page = self.qr_page = self.image_page = None
        self.tool_icons = []
        self._create_main_page()
        self.after(300, self._preload_pages)

    def _create_main_page(self):
        if self.home_page:
            self._show_page(self.home_page)
            return
        self.tool_icons = []
        page = ctk.CTkFrame(self, fg_color=APP_BG)
        self.home_page = page

        header = ctk.CTkFrame(page, fg_color=HEADER_BG, height=88, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="工具箱", font=ui_font(31, "bold"), text_color=INK).pack(side="left", padx=PAGE_MARGIN + SECTION_INSET)
        self.appearance_button = ctk.CTkButton(header, text="深色", font=ui_font(14), text_color=PRIMARY, fg_color="transparent", hover_color=HOVER_SURFACE, width=62, command=self._toggle_appearance)
        self.appearance_button.pack(side="right", padx=28)

        footer = ctk.CTkLabel(page, text=f"UtilBox  ·  版本 {__version__}", font=ui_font(13), text_color=SECONDARY)
        footer.pack(side="bottom", anchor="w", padx=PAGE_MARGIN + SECTION_INSET, pady=(0, 20))

        body = ctk.CTkScrollableFrame(page, fg_color="transparent", scrollbar_button_color=CHEVRON, scrollbar_button_hover_color=SECONDARY)
        body.pack(fill="both", expand=True, padx=PAGE_MARGIN, pady=(27, 0))
        self._tool_group(body, "图像与分享", [
            ("image-converter", "图标生成器", "把图片转换为 ICO 图标", PRIMARY, self._open_icon_generator),
            ("image-converter", "二维码工具", "生成并保存本地二维码", SUCCESS, self._open_qr),
            ("image-converter", "图片压缩与转换", "批量压缩与格式转换", PRIMARY, self._open_image_processor),
        ])
        self._tool_group(body, "网络与系统", [
            ("network-scan", "局域网扫描器", "查找设备并查看开放服务", SUCCESS, self._open_lan_scanner),
            ("network-scan", "本地端口占用", "查看监听端口、PID 与进程", PRIMARY, self._open_port),
        ])
        ctk.CTkFrame(body, fg_color="transparent", height=36).pack(fill="x")

        self._show_page(page)

    def _tool_group(self, parent, title, items):
        ctk.CTkLabel(parent, text=title, font=ui_font(13), text_color=SECONDARY).pack(anchor="w", padx=SECTION_INSET, pady=(0 if title == "图像与分享" else 22, 10))
        group = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=14)
        group.pack(fill="x")
        for index, item in enumerate(items):
            self._tool_row(group, *item)
            if index < len(items) - 1:
                ctk.CTkFrame(group, fg_color=SEPARATOR, height=1).pack(fill="x", padx=(90, ROW_INSET))

    def _tool_row(self, parent, icon_name, title, description, color, command):
        row = ctk.CTkFrame(parent, fg_color=SURFACE, height=76, corner_radius=0)
        row.pack(fill="x")
        row.pack_propagate(False)
        icon = load_icon(icon_name, 38)
        self.tool_icons.append(icon)
        icon_label = ctk.CTkLabel(row, text="", image=icon, width=52, height=52, fg_color=color, corner_radius=12)
        icon_label.place(x=ROW_INSET, y=12)
        title_label = ctk.CTkLabel(row, text=title, font=ui_font(17, "bold"), text_color=INK, anchor="w")
        title_label.place(x=90, y=15)
        description_label = ctk.CTkLabel(row, text=description, font=ui_font(14), text_color=SECONDARY, anchor="w")
        description_label.place(x=90, y=39)
        arrow_label = ctk.CTkLabel(row, text="›", font=ui_font(28), text_color=CHEVRON)
        arrow_label.place(relx=1, x=-42, y=18)

        def on_enter(_event):
            row.configure(fg_color=HOVER_SURFACE)

        def on_leave(_event):
            row.configure(fg_color=SURFACE)

        for widget in (row, icon_label, title_label, description_label, arrow_label):
            widget.bind("<Button-1>", lambda _event: command())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def _open_icon_generator(self):
        if self.icon_page is None:
            self.icon_page = IconGeneratorPage(self, self._create_main_page)
        self._show_page(self.icon_page)

    def _open_lan_scanner(self):
        if self.scanner_page is None:
            self.scanner_page = LanScannerPage(self, self._create_main_page)
        self._show_page(self.scanner_page)

    def _open_port(self):
        self.port_page = self.port_page or PortInspectorPage(self, self._create_main_page); self._show_page(self.port_page)
    def _open_qr(self):
        self.qr_page = self.qr_page or QrPage(self, self._create_main_page); self._show_page(self.qr_page)
    def _open_image_processor(self):
        self.image_page = self.image_page or ImageProcessorPage(self, self._create_main_page); self._show_page(self.image_page)

    def _show_page(self, page):
        """Swap cached pages without rebuilding their widget trees."""
        if self.current_page and self.current_page is not page:
            self.current_page.pack_forget()
        page.pack(fill="both", expand=True)
        self.current_page = page

    def _preload_pages(self):
        """Build tool pages after the launcher has become visible."""
        if self.icon_page is None:
            self.icon_page = IconGeneratorPage(self, self._create_main_page)
        if self.scanner_page is None:
            self.scanner_page = LanScannerPage(self, self._create_main_page)

    def _toggle_appearance(self):
        self.appearance_mode = "dark" if self.appearance_mode == "light" else "light"
        ctk.set_appearance_mode(self.appearance_mode)
        self.appearance_button.configure(text="浅色" if self.appearance_mode == "dark" else "深色")


if __name__ == "__main__":
    ToolboxApp().mainloop()
