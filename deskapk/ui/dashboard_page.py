import tkinter as tk

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # Header
        header = tk.Frame(self, bg="#343a40", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Live Attendance Scanner", font=("Arial", 16, "bold"), 
                 bg="#343a40", fg="white").pack(pady=15)

        # Content Layout
        content = tk.Frame(self, bg="#f4f6f9")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        # Left Side: Camera Placeholder
        self.cam_label = tk.Label(content, text="Initializing Camera...", bg="black", 
                                  fg="white", width=60, height=20)
        self.cam_label.grid(row=0, column=0, padx=10)

        # Right Side: Quick Stats
        stats_frame = tk.LabelFrame(content, text=" Session Statistics ", font=("Arial", 12, "bold"), 
                                    bg="white", padx=20, pady=20)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        self.total_lbl = tk.Label(stats_frame, text="Total Present: 0", font=("Arial", 14), bg="white")
        self.total_lbl.pack(anchor="w", pady=5)
        
        self.last_scan_lbl = tk.Label(stats_frame, text="Last Scan: None", font=("Arial", 11), 
                                      bg="white", fg="#007bff")
        self.last_scan_lbl.pack(anchor="w", pady=20)

        # Back Button
        tk.Button(self, text="Return to Menu", command=lambda: controller.show_frame("HomePage"),
                  bg="#6c757d", fg="white", font=("Arial", 10), width=15).pack(pady=20)