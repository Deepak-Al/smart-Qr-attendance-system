import tkinter as tk

class QRPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="QR Code Generator", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="(QR generation logic will be added later)").pack(pady=10)

        tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame("HomePage")
        ).pack(pady=30)
