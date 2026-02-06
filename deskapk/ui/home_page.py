import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(
            self,
            text="Smart QR Attendance System",
            font=("Arial", 24, "bold")
        ).pack(pady=40)

        tk.Button(
            self,
            text="Generate QR Code",
            width=30,
            height=2,
            command=lambda: controller.show_frame("QRPage")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Attendance Dashboard",
            width=30,
            height=2,
            command=lambda: controller.show_frame("DashboardPage")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Reports & Excel Export",
            width=30,
            height=2,
            command=lambda: controller.show_frame("ReportPage")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Exit",
            width=30,
            height=2,
            command=controller.quit
        ).pack(pady=30)
