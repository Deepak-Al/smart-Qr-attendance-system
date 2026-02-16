# ui/dashboard_page.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from core.scanner import QRScanner
from database.db_manager import DatabaseManager

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller
        self.db = DatabaseManager()
        self.scanner = QRScanner(self.db)

        # 1. TOP HEADER
        header = tk.Frame(self, bg="#343a40", height=50)
        header.pack(side="top", fill="x")
        tk.Label(header, text="Attendance Terminal", font=("Arial", 14, "bold"), bg="#343a40", fg="white").pack(pady=10)

        # 2. LEFT SIDEBAR (Controls & Stats)
        sidebar = tk.Frame(self, bg="#ffffff", width=300, relief="flat")
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False) # Maintain width

        tk.Label(sidebar, text="System Controls", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=20)

        self.start_btn = tk.Button(sidebar, text="START CAMERA", bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                                   height=2, command=self.start_scanning)
        self.start_btn.pack(fill="x", padx=20, pady=5)

        tk.Button(sidebar, text="STOP CAMERA", bg="#dc3545", fg="white", command=self.stop_scanning).pack(fill="x", padx=20, pady=5)

        # Session Stats
        tk.Label(sidebar, text="--- Statistics ---", bg="#ffffff", font=("Arial", 10, "italic")).pack(pady=(30, 10))
        self.status_lbl = tk.Label(sidebar, text="Status: Ready", font=("Arial", 10), bg="#ffffff", fg="blue")
        self.status_lbl.pack(pady=5)
        
        self.count_lbl = tk.Label(sidebar, text="Present: 0", font=("Arial", 16, "bold"), bg="#ffffff")
        self.count_lbl.pack(pady=10)

        # THE "BACK" BUTTON - Fixed position at bottom of sidebar
        tk.Button(sidebar, text="⬅ Back to Menu", font=("Arial", 10), bg="#6c757d", fg="white", 
                  command=self.go_back).pack(side="bottom", fill="x", padx=20, pady=30)

        # 3. RIGHT MAIN AREA (Camera Feed)
        self.cam_area = tk.Label(self, bg="#000000", text="Camera Offline", fg="white", font=("Arial", 12))
        self.cam_area.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    def start_scanning(self):
        if not self.scanner.is_running:
            if self.scanner.start_camera():
                self.start_btn.config(state="disabled")
                self.update_frame()
            else:
                messagebox.showerror("Camera Error", "No camera detected. Please check your USB connection.")

    def stop_scanning(self):
        self.scanner.stop_camera()
        self.start_btn.config(state="normal")
        self.cam_area.config(image="", text="Camera Offline")
        self.status_lbl.config(text="Status: Ready", fg="blue")

    def update_frame(self):
        if self.scanner.is_running:
            frame, status, name = self.scanner.process_frame()
            
            # Update status even if no name is scanned
            self.status_lbl.config(text=f"Status: {status}")
            if name:
                self.count_lbl.config(text=f"Present: {self.db.get_daily_stats()}")

            if frame is not None:
                # Convert frame for Tkinter
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                # Auto-resize to fit the current window size
                w = self.cam_area.winfo_width()
                h = self.cam_area.winfo_height()
                if w > 100 and h > 100: # Ensure valid dimensions
                    img = img.resize((w, h), Image.Resampling.LANCZOS)
                
                img_tk = ImageTk.PhotoImage(image=img)
                self.cam_area.img_tk = img_tk
                self.cam_area.config(image=img_tk)
            
            self.after(15, self.update_frame)

    def go_back(self):
        self.stop_scanning()
        self.controller.show_frame("HomePage")