import tkinter as tk
from datetime import datetime


class ConsolePanel(tk.Frame):
    def __init__(self, master, theme: dict = None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#1a1a2e"), **kwargs)
        self._max_lines = 300
        self._build()

    def _build(self):
        t = self._theme

        header = tk.Frame(self, bg=t.get("bg_header", "#16213e"))
        header.pack(fill="x", padx=2, pady=(2, 0))
        tk.Label(
            header, text="📋 日志", bg=t.get("bg_header", "#16213e"),
            fg=t.get("text_primary", "#e0e0e0"),
            font=("Microsoft YaHei UI", 10, "bold"), anchor="w",
        ).pack(side="left", padx=8, pady=2)

        self._show_debug = False
        self._debug_btn = tk.Button(
            header, text="Debug", bg=t.get("bg_button", "#0f3460"),
            fg=t.get("text_muted", "#666666"),
            activebackground=t.get("bg_button_hover", "#1a5276"),
            activeforeground=t.get("text_primary", "#ffffff"),
            font=("Microsoft YaHei UI", 9), relief="flat", cursor="hand2",
            command=self._toggle_debug,
        )
        self._debug_btn.pack(side="right", padx=(0, 4), pady=2)

        self._clear_btn = tk.Button(
            header, text="清空", bg=t.get("bg_button", "#0f3460"),
            fg=t.get("text_primary", "#e0e0e0"),
            activebackground=t.get("bg_button_hover", "#1a5276"),
            activeforeground=t.get("text_primary", "#ffffff"),
            font=("Microsoft YaHei UI", 9), relief="flat", cursor="hand2",
            command=self._clear,
        )
        self._clear_btn.pack(side="right", padx=8, pady=2)

        self._text = tk.Text(
            self, bg=t.get("console_bg", "#0a0a1a"),
            fg=t.get("console_text", "#b0b0b0"),
            font=("Consolas", 9), relief="flat", wrap="word",
            insertbackground=t.get("text_primary", "#e0e0e0"),
            selectbackground=t.get("bg_button", "#0f3460"),
            state="disabled", height=8,
        )
        self._scrollbar = tk.Scrollbar(
            self, command=self._text.yview,
            bg=t.get("bg_header", "#16213e"),
            troughcolor=t.get("bg_panel", "#1a1a2e"),
        )
        self._text.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)
        self._text.pack(side="left", fill="both", expand=True, padx=(2, 0), pady=2)

        self._apply_tags()

    def _apply_tags(self):
        t = self._theme
        self._text.tag_configure("timestamp", foreground=t.get("text_muted", "#666666"))
        self._text.tag_configure("info", foreground=t.get("accent_blue", "#4fc3f7"))
        self._text.tag_configure("warning", foreground=t.get("accent_orange", "#ffb74d"))
        self._text.tag_configure("error", foreground=t.get("accent_red", "#ef5350"))
        self._text.tag_configure("shock", foreground=t.get("accent_purple", "#e040fb"))
        self._text.tag_configure("recv", foreground=t.get("accent_green", "#66bb6a"))
        self._text.tag_configure("debug", foreground=t.get("text_muted", "#666666"))

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#1a1a2e"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_panel", "#1a1a2e")
                fg = t.get("text_primary", "#e0e0e0")
                if isinstance(w, tk.Text):
                    w.configure(bg=t.get("console_bg", "#0a0a1a"),
                                fg=t.get("console_text", "#b0b0b0"),
                                insertbackground=fg,
                                selectbackground=t.get("bg_button", "#0f3460"))
                elif isinstance(w, tk.Button):
                    w.configure(bg=t.get("bg_button", "#0f3460"), fg=fg,
                                activebackground=t.get("bg_button_hover", "#1a5276"))
                elif isinstance(w, tk.Scrollbar):
                    w.configure(bg=t.get("bg_header", "#16213e"),
                                troughcolor=t.get("bg_panel", "#1a1a2e"))
                elif isinstance(w, tk.Frame):
                    w.configure(bg=t.get("bg_header", "#16213e"))
                elif isinstance(w, tk.Label):
                    w.configure(bg=t.get("bg_header", "#16213e"), fg=fg)
            except (tk.TclError, KeyError):
                pass
        self._apply_tags()

    def _get_all_widgets(self):
        widgets = []
        stack = [self]
        while stack:
            w = stack.pop()
            widgets.append(w)
            stack.extend(w.winfo_children())
        return widgets

    def append(self, text: str, tag: str = "info"):
        if tag == "debug" and not self._show_debug:
            return
        now = datetime.now().strftime("%H:%M:%S")
        self._text.configure(state="normal")
        self._text.insert("end", f"[{now}] ", "timestamp")
        self._text.insert("end", f"{text}\n", tag)
        line_count = int(self._text.index("end-1c").split(".")[0])
        if line_count > self._max_lines:
            self._text.delete("1.0", f"{line_count - self._max_lines}.0")
        self._text.see("end")
        self._text.configure(state="disabled")

    def _toggle_debug(self):
        self._show_debug = not self._show_debug
        t = self._theme
        if self._show_debug:
            self._debug_btn.configure(fg=t.get("accent_cyan", "#39d2c0"))
        else:
            self._debug_btn.configure(fg=t.get("text_muted", "#666666"))

    def _clear(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")
