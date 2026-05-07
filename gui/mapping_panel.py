import tkinter as tk


class MappingPanel(tk.Frame):
    def __init__(self, master, theme: dict = None, on_mapping_change=None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#1a1a2e"), **kwargs)
        self._on_change = on_mapping_change or (lambda: None)
        self._sliders: dict[int, tk.Scale] = {}
        self._labels: dict[int, tk.Label] = {}
        self._build()

    def _build(self):
        t = self._theme

        # Header
        header = tk.Frame(self, bg=t.get("bg_header", "#16213e"))
        header.pack(fill="x", padx=2, pady=(2, 0))
        tk.Label(
            header, text="📊 秒数-强度映射", bg=t.get("bg_header", "#16213e"),
            fg=t.get("text_primary", "#e0e0e0"),
            font=("Microsoft YaHei UI", 10, "bold"), anchor="w",
        ).pack(side="left", padx=8, pady=4)

        # Mapping rows (1-10 seconds)
        mapping_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        mapping_frame.pack(fill="x", padx=8, pady=4)

        default_mapping = {
            1: 30, 2: 50, 3: 200, 4: 80, 5: 100,
            6: 120, 7: 150, 8: 170, 9: 185, 10: 200,
        }

        for sec in range(1, 11):
            row = tk.Frame(mapping_frame, bg=t.get("bg_panel", "#1a1a2e"))
            row.pack(fill="x", pady=0)

            label_text = f"{sec}s:"
            if sec == 3:
                label_text = "3s:"
            lbl = tk.Label(
                row, text=label_text, bg=t.get("bg_panel", "#1a1a2e"),
                fg=t.get("text_secondary", "#b0b0b0"),
                font=("Consolas", 9), width=3, anchor="e",
            )
            lbl.pack(side="left")

            var = tk.IntVar(value=default_mapping[sec])
            val_label = tk.Label(
                row, text=str(default_mapping[sec]), bg=t.get("bg_panel", "#1a1a2e"),
                fg=t.get("text_primary", "#e0e0e0"),
                font=("Consolas", 9), width=4, anchor="w",
            )
            val_label.pack(side="right")

            slider = tk.Scale(
                row, from_=0, to=200, orient="horizontal",
                variable=var, command=lambda v, s=sec: self._on_slider_change(s, v),
                bg=t.get("bg_panel", "#1a1a2e"),
                fg=t.get("text_dim", "#888888"),
                troughcolor=t.get("bg_slider_trough", "#0f3460"),
                highlightthickness=0, sliderrelief="flat", length=120,
                showvalue=False,
            )
            slider.pack(side="right", padx=(4, 4))

            self._sliders[sec] = slider
            self._labels[sec] = val_label

        # Reset button
        btn_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        btn_frame.pack(fill="x", padx=8, pady=(4, 8))

        self._reset_btn = tk.Button(
            btn_frame, text="重置默认", bg=t.get("bg_button_danger", "#4a1a1a"),
            fg=t.get("text_primary", "#e0e0e0"),
            activebackground=t.get("bg_button_danger_hover", "#6a2a2a"),
            activeforeground=t.get("text_primary", "#ffffff"),
            font=("Microsoft YaHei UI", 9), relief="flat", cursor="hand2",
            command=self._reset_defaults,
        )
        self._reset_btn.pack(side="right")

    def _on_slider_change(self, sec: int, value: str):
        val = int(float(value))
        self._labels[sec].configure(text=str(val))
        self._on_change()

    def _reset_defaults(self):
        defaults = {
            1: 30, 2: 50, 3: 200, 4: 80, 5: 100,
            6: 120, 7: 150, 8: 170, 9: 185, 10: 200,
        }
        for sec, val in defaults.items():
            self._sliders[sec].set(val)
            self._labels[sec].configure(text=str(val))
        self._on_change()

    def get_mapping(self) -> dict[str, int]:
        return {str(s): self._sliders[s].get() for s in range(1, 11)}

    def set_mapping(self, mapping: dict):
        for sec in range(1, 11):
            key = str(sec)
            if key in mapping:
                val = int(mapping[key])
                self._sliders[sec].set(val)
                self._labels[sec].configure(text=str(val))

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#1a1a2e"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_panel", "#1a1a2e")
                if isinstance(w, tk.Scale):
                    w.configure(bg=bg, fg=t.get("text_dim", "#888888"),
                                troughcolor=t.get("bg_slider_trough", "#0f3460"))
                elif isinstance(w, tk.Button):
                    w.configure(bg=t.get("bg_button_danger", "#4a1a1a"),
                                fg=t.get("text_primary", "#e0e0e0"),
                                activebackground=t.get("bg_button_danger_hover", "#6a2a2a"))
                elif isinstance(w, tk.Frame):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Label):
                    w.configure(bg=bg, fg=t.get("text_secondary", "#b0b0b0"))
            except (tk.TclError, KeyError):
                pass

    def _get_all_widgets(self):
        widgets = []
        stack = [self]
        while stack:
            w = stack.pop()
            widgets.append(w)
            stack.extend(w.winfo_children())
        return widgets
