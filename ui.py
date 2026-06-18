import os
import sys
import threading
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from tkinter import font as tkfont

# Ensure FAQ dataset resolves when launched from any working directory
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)
os.chdir(_APP_DIR)

from chat import get_answer

# ── Theme ──────────────────────────────────────────────────────────────────
BG = "#0f1320"
SECONDARY = "#181c2d"
CONTRAST = "#202940"
ACCENT = "#5865F2"
TEXT = "#e8e9f3"
GREY = "#9aa0b0"
BOT_BUBBLE = "#212944"
USER_BUBBLE = "#4a5fc1"
INPUT_BORDER = "#2d3350"
SIDEBAR_ACCENT = "#7289da"

WINDOW_W, WINDOW_H = 480, 700
WELCOME = "Yohohoho! I'm Mugiwara Bot. Ask me anything about your order! 🎩"

QUICK_REPLIES = [
    "Track my order",
    "Return policy",
    "Payment methods",
    "Shipping time",
]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def draw_straw_hat(canvas: tk.Canvas, cx: int, cy: int, scale: float = 1.0) -> None:
    """Draw Luffy-style straw hat icon on a tkinter Canvas (matches assets/straw_hat.svg)."""
    s = scale
    canvas.create_oval(
        cx - 14 * s, cy + 2 * s, cx + 14 * s, cy + 10 * s,
        fill="#D4A853", outline="#8B6914", width=max(1, int(1.5 * s)),
    )
    canvas.create_polygon(
        cx - 12 * s, cy + 2 * s,
        cx, cy - 14 * s,
        cx + 12 * s, cy + 2 * s,
        cx + 10 * s, cy + 6 * s,
        cx, cy - 4 * s,
        cx - 10 * s, cy + 6 * s,
        fill="#D4A853", outline="#8B6914", width=max(1, int(1.5 * s)),
    )
    canvas.create_polygon(
        cx - 10 * s, cy,
        cx, cy - 10 * s,
        cx + 10 * s, cy,
        cx + 9 * s, cy + 4 * s,
        cx, cy - 2 * s,
        cx - 9 * s, cy + 4 * s,
        fill="#CC0000", outline="",
    )


class MugiwaraFAQBot(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Mugiwara FAQ Bot")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.minsize(WINDOW_W, WINDOW_H)
        self.resizable(True, True)
        self.configure(fg_color=BG)

        self._typing_frame = None
        self._pulse_step = 0
        self._busy = False

        self._title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self._subtitle_font = tkfont.Font(family="Segoe UI", size=10)
        self._msg_font = tkfont.Font(family="Segoe UI", size=11)
        self._time_font = tkfont.Font(family="Segoe UI", size=8)
        self._btn_font = tkfont.Font(family="Segoe UI", size=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()
        self._bind_events()

        self.after(200, self._show_welcome)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(self, fg_color=SECONDARY, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw", padx=(15, 0), pady=15)
        sidebar.grid_rowconfigure(5, weight=1)

        top_block = ctk.CTkFrame(sidebar, fg_color=SECONDARY, corner_radius=0)
        top_block.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

        logo = tk.Canvas(top_block, width=40, height=40, bg=SECONDARY, highlightthickness=0)
        logo.pack(side="left", padx=(0, 12))
        draw_straw_hat(logo, 20, 22, scale=1.0)

        ctk.CTkLabel(
            top_block,
            text="Mugiwara",
            font=self._title_font,
            text_color=TEXT,
            fg_color=SECONDARY,
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            top_block,
            text="FAQ Chat",
            font=self._subtitle_font,
            text_color=GREY,
            fg_color=SECONDARY,
            anchor="w",
        ).pack(anchor="w")

        section_label = ctk.CTkLabel(
            sidebar,
            text="FAQ Topics",
            font=self._subtitle_font,
            text_color=GREY,
            fg_color=SECONDARY,
            anchor="w",
        )
        section_label.grid(row=1, column=0, sticky="w", padx=16, pady=(12, 6))

        for index, label in enumerate(QUICK_REPLIES, start=2):
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                font=self._btn_font,
                text_color=TEXT,
                fg_color=CONTRAST,
                hover_color=SIDEBAR_ACCENT,
                corner_radius=12,
                height=40,
                command=lambda t=label: self.send_message(t),
            )
            btn.grid(row=index, column=0, sticky="ew", padx=16, pady=4)

        footer = ctk.CTkFrame(sidebar, fg_color=SECONDARY, corner_radius=0)
        footer.grid(row=6, column=0, sticky="ew", padx=16, pady=(16, 16))

        ctk.CTkLabel(
            footer,
            text="Online",
            font=self._subtitle_font,
            text_color=GREY,
            fg_color=SECONDARY,
            anchor="w",
        ).pack(side="left")

    # ── Main area ────────────────────────────────────────────────────────────
    def _build_main_area(self) -> None:
        main_area = ctk.CTkFrame(self, fg_color=BG)
        main_area.grid(row=0, column=1, sticky="nsew", padx=(15, 15), pady=15)
        main_area.grid_rowconfigure(1, weight=1)
        main_area.grid_columnconfigure(0, weight=1)

        self._build_header(main_area)
        self._build_chat(main_area)
        self._build_quick_replies(main_area)
        self._build_input(main_area)

    # ── Header ───────────────────────────────────────────────────────────────
    def _build_header(self, parent: ctk.CTkFrame) -> None:
        header = ctk.CTkFrame(parent, fg_color=SECONDARY, corner_radius=16, height=90)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 12))
        header.grid_columnconfigure(0, weight=1)

        title_block = ctk.CTkFrame(header, fg_color=SECONDARY, corner_radius=0)
        title_block.grid(row=0, column=0, sticky="w", padx=20, pady=16)

        ctk.CTkLabel(
            title_block,
            text="Mugiwara FAQ Bot",
            font=self._title_font,
            text_color=TEXT,
            fg_color=SECONDARY,
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="Your e-commerce assistant with a sleek Discord-inspired layout.",
            font=self._subtitle_font,
            text_color=GREY,
            fg_color=SECONDARY,
            anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        self._theme_btn = ctk.CTkButton(
            header,
            text="Toggle Theme",
            font=self._btn_font,
            text_color=TEXT,
            fg_color=CONTRAST,
            hover_color=SIDEBAR_ACCENT,
            corner_radius=14,
            width=130,
            command=self._toggle_theme,
        )
        self._theme_btn.grid(row=0, column=1, sticky="e", padx=20, pady=20)

    def _toggle_theme(self) -> None:
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if mode == "dark" else "dark")

    # ── Chat area ────────────────────────────────────────────────────────────
    def _build_chat(self, parent: ctk.CTkFrame) -> None:
        chat_wrapper = ctk.CTkFrame(parent, fg_color=CONTRAST, corner_radius=20)
        chat_wrapper.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 12))
        chat_wrapper.grid_rowconfigure(0, weight=1)
        chat_wrapper.grid_columnconfigure(0, weight=1)

        self._messages_frame = ctk.CTkScrollableFrame(
            chat_wrapper,
            fg_color=CONTRAST,
            border_width=0,
            corner_radius=20,
        )
        self._messages_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self._messages_frame.grid_columnconfigure(0, weight=1)

    def _scroll_to_bottom(self) -> None:
        self._messages_frame.update_idletasks()
        try:
            self._messages_frame._canvas.yview_moveto(1.0)
        except AttributeError:
            pass

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M")

    def _add_bot_message(self, text: str) -> None:
        row = ctk.CTkFrame(self._messages_frame, fg_color=CONTRAST, corner_radius=0)
        row.pack(fill="x", padx=8, pady=(10, 2), anchor="w")

        avatar = tk.Canvas(row, width=32, height=32, bg=CONTRAST, highlightthickness=0)
        avatar.pack(side="left", anchor="n", padx=(0, 10), pady=4)
        draw_straw_hat(avatar, 16, 18, scale=0.85)

        bubble = ctk.CTkFrame(row, fg_color=BOT_BUBBLE, corner_radius=18)
        bubble.pack(side="left", anchor="w")

        ctk.CTkLabel(
            bubble,
            text=text,
            font=self._msg_font,
            text_color=TEXT,
            fg_color=BOT_BUBBLE,
            wraplength=420,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(
            row,
            text=self._timestamp(),
            font=self._time_font,
            text_color=GREY,
            fg_color=CONTRAST,
        ).pack(side="left", padx=(10, 0), pady=18)

        self._scroll_to_bottom()

    def _add_user_message(self, text: str) -> None:
        row = ctk.CTkFrame(self._messages_frame, fg_color=CONTRAST, corner_radius=0)
        row.pack(fill="x", padx=8, pady=(10, 2))

        bubble = ctk.CTkFrame(row, fg_color=USER_BUBBLE, corner_radius=18)
        bubble.pack(side="right", anchor="e")

        ctk.CTkLabel(
            bubble,
            text=text,
            font=self._msg_font,
            text_color=TEXT,
            fg_color=USER_BUBBLE,
            wraplength=420,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(
            row,
            text=self._timestamp(),
            font=self._time_font,
            text_color=GREY,
            fg_color=CONTRAST,
        ).pack(side="right", padx=(0, 10), pady=18)

        self._scroll_to_bottom()

    # ── Typing indicator ─────────────────────────────────────────────────────
    def _show_typing(self) -> None:
        self._hide_typing()
        row = ctk.CTkFrame(self._messages_frame, fg_color=CONTRAST, corner_radius=0)
        row.pack(fill="x", padx=8, pady=(10, 2), anchor="w")
        self._typing_frame = row

        avatar = tk.Canvas(row, width=32, height=32, bg=CONTRAST, highlightthickness=0)
        avatar.pack(side="left", anchor="n", padx=(0, 10), pady=4)
        draw_straw_hat(avatar, 16, 18, scale=0.85)

        bubble = ctk.CTkFrame(row, fg_color=BOT_BUBBLE, corner_radius=18)
        bubble.pack(side="left", anchor="w")

        ctk.CTkFrame(bubble, fg_color=ACCENT, width=4, corner_radius=0).pack(side="left", fill="y")

        dots_frame = ctk.CTkFrame(bubble, fg_color=BOT_BUBBLE, corner_radius=0)
        dots_frame.pack(side="left", padx=14, pady=14)

        self._dot_labels = []
        for _ in range(3):
            dot = ctk.CTkLabel(
                dots_frame,
                text="●",
                font=("Segoe UI", 10),
                text_color=ACCENT,
                fg_color=BOT_BUBBLE,
            )
            dot.pack(side="left", padx=4)
            self._dot_labels.append(dot)

        self._typing_phase = 0
        self._animate_typing()
        self._scroll_to_bottom()

    def _animate_typing(self) -> None:
        if self._typing_frame is None or not self._typing_frame.winfo_exists():
            return
        offsets = [0, 3, 0]
        phase = self._typing_phase % 3
        for i, dot in enumerate(self._dot_labels):
            active = (i + self._typing_phase) % 3 == phase
            dot.configure(text_color=ACCENT if active else "#35478c")
            dot.pack_configure(pady=(0, offsets[(i + self._typing_phase) % 3]))
        self._typing_phase += 1
        self.after(280, self._animate_typing)

    def _hide_typing(self) -> None:
        if self._typing_frame is not None and self._typing_frame.winfo_exists():
            self._typing_frame.destroy()
        self._typing_frame = None

    # ── Quick replies ───────────────────────────────────────────────────────
    def _build_quick_replies(self, parent: ctk.CTkFrame) -> None:
        bar = ctk.CTkFrame(parent, fg_color=SECONDARY, corner_radius=16)
        bar.grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 12))

        for label in QUICK_REPLIES:
            btn = ctk.CTkButton(
                bar,
                text=label,
                font=self._btn_font,
                text_color=TEXT,
                fg_color=CONTRAST,
                hover_color=SIDEBAR_ACCENT,
                corner_radius=14,
                height=38,
                command=lambda t=label: self.send_message(t),
            )
            btn.pack(side="left", padx=8, pady=12, expand=True)

    # ── Input area ───────────────────────────────────────────────────────────
    def _build_input(self, parent: ctk.CTkFrame) -> None:
        input_frame = ctk.CTkFrame(parent, fg_color=SECONDARY, corner_radius=20)
        input_frame.grid(row=3, column=0, sticky="ew", padx=0, pady=(0, 0))
        input_frame.grid_columnconfigure(0, weight=1)

        self._entry = ctk.CTkEntry(
            input_frame,
            font=self._msg_font,
            placeholder_text="Type your question...",
            text_color=TEXT,
            fg_color=CONTRAST,
            border_width=0,
            corner_radius=18,
        )
        self._entry.grid(row=0, column=0, sticky="ew", padx=(16, 10), pady=14)

        self._send_btn = ctk.CTkButton(
            input_frame,
            text="➤",
            width=54,
            height=42,
            fg_color=ACCENT,
            hover_color="#4754da",
            text_color=TEXT,
            corner_radius=18,
            command=self._on_send_click,
        )
        self._send_btn.grid(row=0, column=1, padx=(0, 16), pady=14)

    def _bind_events(self) -> None:
        self._entry.bind("<Return>", lambda _e: self._on_send_click())
        self.bind("<Return>", lambda _e: self._on_send_click())

    def _on_send_click(self) -> None:
        if self._busy:
            return
        text = self._entry.get().strip()
        if not text:
            return
        self._entry.delete(0, tk.END)
        self.send_message(text)

    def _show_welcome(self) -> None:
        self._add_bot_message(WELCOME)

    # ── Core send logic ───────────────────────────────────────────────────────
    def send_message(self, user_input: str) -> None:
        user_input = user_input.strip()
        if not user_input or self._busy:
            return

        self._busy = True
        self._add_user_message(user_input)
        self._show_typing()

        result = {"answer": None}

        def fetch_answer() -> None:
            result["answer"] = get_answer(user_input)

        thread = threading.Thread(target=fetch_answer, daemon=True)
        thread.start()

        def reveal(min_delay_done: bool = False) -> None:
            if not min_delay_done:
                self.after(1000, lambda: reveal(True))
                return
            if thread.is_alive():
                self.after(50, lambda: reveal(True))
                return
            self._hide_typing()
            self._add_bot_message(result["answer"])
            self._busy = False

        self.after(1000, lambda: reveal(True))


def main() -> None:
    app = MugiwaraFAQBot()
    app.mainloop()


if __name__ == "__main__":
    main()
