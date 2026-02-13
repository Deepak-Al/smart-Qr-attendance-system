import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        # Title Section
        tk.Label(
            self, 
            text="Attendance Management System", 
            font=("Arial", 28, "bold"), 
            bg="#ffffff", 
            fg="#333"
        ).pack(pady=(60, 10))

        tk.Label(
            self, 
            text="Secure • Fast • Automated", 
            font=("Arial", 12), 
            bg="#ffffff", 
            fg="#666"
        ).pack(pady=(0, 40))

        # Button Style Config
        btn_opts = {"width": 25, "height": 2, "font": ("Arial", 12), "cursor": "hand2"}

        # Navigation Buttons
        tk.Button(self, text="Live Scanner", bg="#007bff", fg="white", 
                  command=lambda: controller.show_frame("DashboardPage"), **btn_opts).pack(pady=10)
        
        tk.Button(self, text="Student Registration (QR)", bg="#28a745", fg="white", 
                  command=lambda: controller.show_frame("QRPage"), **btn_opts).pack(pady=10)
        
        tk.Button(self, text="View Reports", bg="#6c757d", fg="white", 
                  command=lambda: controller.show_frame("ReportPage"), **btn_opts).pack(pady=10)
        
        tk.Button(self, text="Exit System", bg="#dc3545", fg="white", 
                  command=controller.quit, **btn_opts).pack(pady=(30, 0))