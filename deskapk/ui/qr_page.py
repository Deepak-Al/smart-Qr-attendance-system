import tkinter as tk

class QRPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="Student Registration", font=("Arial", 22, "bold"), bg="#ffffff").pack(pady=30)

        # Form Container
        form = tk.Frame(self, bg="#ffffff")
        form.pack(pady=10)

        tk.Label(form, text="Full Name:", bg="#ffffff", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form, width=30, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form, text="Registration ID:", bg="#ffffff", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.reg_entry = tk.Entry(form, width=30, font=("Arial", 12))
        self.reg_entry.grid(row=1, column=1, pady=5, padx=10)

        # Actions
        tk.Button(self, text="Generate & Save ID", bg="#28a745", fg="white", 
                  font=("Arial", 12, "bold"), width=25, height=2).pack(pady=20)

        # Preview Area
        self.qr_preview = tk.Label(self, text="QR Preview will appear here", bg="#f8f9fa", 
                                   width=30, height=10, relief="sunken")
        self.qr_preview.pack(pady=10)

        tk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage"), 
                  bg="#6c757d", fg="white", width=10).pack(pady=20)