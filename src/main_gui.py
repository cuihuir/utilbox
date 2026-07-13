"""多功能小工具集合 - 主界面"""
import customtkinter as ctk
from icon_generator import IconGeneratorPage
from lan_scanner import LanScannerPage
from ui_style import UI_FONT_FAMILY, load_icon, ui_font


class ToolboxApp(ctk.CTk):
    """多功能工具箱主应用"""

    def __init__(self):
        super().__init__()

        # 窗口配置
        self.title("多功能工具箱")
        self.geometry("800x600")
        self.resizable(True, True)
        self.minsize(700, 500)

        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 当前页面
        self.current_page = None
        self.tool_icons = []

        # 创建主界面
        self._create_main_page()

    def _create_main_page(self):
        """创建主界面"""
        # 清除当前页面
        if self.current_page:
            self.current_page.destroy()
        self.tool_icons = []

        # 创建主容器
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_page = main_frame

        # 标题
        title = ctk.CTkLabel(
            main_frame,
            text="多功能工具箱",
            font=ui_font(size=32, weight="bold")
        )
        title.pack(pady=(40, 20))

        subtitle = ctk.CTkLabel(
            main_frame,
            text="选择一个工具开始使用",
            font=ui_font(size=14),
            text_color="#888888"
        )
        subtitle.pack(pady=(0, 40))

        # 工具卡片容器
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(expand=True, fill="both", padx=40)

        # 配置网格布局（2列）
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        # 工具1: 图标生成器
        self._create_tool_card(
            cards_frame,
            row=0, col=0,
            icon_name="image-converter",
            title="图标生成器",
            description="将PNG/JPG等图片转换为ICO格式\n支持多尺寸图标生成",
            command=self._open_icon_generator,
            color="#5B8DEE"
        )

        # 工具2: 局域网扫描器
        self._create_tool_card(
            cards_frame,
            row=0, col=1,
            icon_name="network-scan",
            title="局域网扫描器",
            description="扫描局域网内的活跃主机\n检测开放端口和服务",
            command=self._open_lan_scanner,
            color="#2ECC71"
        )

        # 底部信息
        footer = ctk.CTkLabel(
            main_frame,
            text="v1.0.0 | 更多工具持续添加中...",
            font=ui_font(size=11),
            text_color="#666666"
        )
        footer.pack(side="bottom", pady=20)

    def _create_tool_card(self, parent, row, col, icon_name, title, description, command, color):
        """创建工具卡片"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#2b2b2b",
            corner_radius=15
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # 图标
        icon_label = ctk.CTkLabel(
            card,
            text="",
            image=load_icon(icon_name, 52)
        )
        self.tool_icons.append(icon_label.cget("image"))
        icon_label.pack(pady=(30, 10))

        # 标题
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ui_font(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        # 描述
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ui_font(size=12),
            text_color="#aaaaaa",
            justify="center"
        )
        desc_label.pack(pady=(0, 20), padx=20)

        # 打开按钮
        open_btn = ctk.CTkButton(
            card,
            text="打开工具",
            command=command,
            font=ui_font(size=14, weight="bold"),
            height=40,
            fg_color=color,
            hover_color=self._darken_color(color)
        )
        open_btn.pack(pady=(0, 30), padx=40, fill="x")

    def _darken_color(self, hex_color):
        """将颜色变暗"""
        # 简单的颜色变暗算法
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _open_icon_generator(self):
        """打开图标生成器"""
        if self.current_page:
            self.current_page.destroy()

        self.current_page = IconGeneratorPage(self, self._create_main_page)
        self.current_page.pack(fill="both", expand=True)

    def _open_lan_scanner(self):
        """打开局域网扫描器"""
        if self.current_page:
            self.current_page.destroy()

        self.current_page = LanScannerPage(self, self._create_main_page)
        self.current_page.pack(fill="both", expand=True)


def main():
    """主函数"""
    app = ToolboxApp()
    app.mainloop()


if __name__ == "__main__":
    main()
