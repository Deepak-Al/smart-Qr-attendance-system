import tkinter as tk

class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Attendance Reports", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="(Preview & Excel export will be added)").pack(pady=10)

        tk.Button(
            self,
            text="Export to Excel",
            width=20
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame("HomePage")
        ).pack(pady=20)
