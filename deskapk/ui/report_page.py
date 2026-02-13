import tkinter as tk
from ui.styles import *

class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(
            self,
            text="Attendance Reports",
            font=HEADER_FONT,
            bg=BG_COLOR,
            fg=PRIMARY
        ).pack(pady=20)

        box = tk.Frame(self, bg=CARD_BG, padx=30, pady=30)
        box.pack()

        tk.Label(
            box,
            text="Preview attendance records here",
            bg=CARD_BG
        ).pack(pady=10)

        tk.Button(
            box,
            text="Export to Excel",
            font=BUTTON_FONT,
            bg=ACCENT,
            fg="white",
            width=20,
            bd=0
        ).pack(pady=15)

        tk.Button(
            self,
            text="← Back",
            font=BUTTON_FONT,
            bg=PRIMARY,
            fg="white",
            bd=0,
            command=lambda: controller.show_frame("HomePage")
        ).pack(pady=20)
