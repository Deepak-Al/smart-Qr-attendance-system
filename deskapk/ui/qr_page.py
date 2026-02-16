# ui/qr_page.py (REVISED)
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import os
from PIL import Image, ImageTk
from core.generator import QRGenerator
from database.db_manager import DatabaseManager

class QRPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.db = DatabaseManager()
        self.generator = QRGenerator()
        self.last_generated_path = None

        tk.Label(self, text="Student Registration", font=("Arial", 22, "bold"), bg="#ffffff").pack(pady=20)

        # Form
        form = tk.Frame(self, bg="#ffffff")
        form.pack(pady=5)
        self.name_entry = self._create_input(form, "Full Name:", 0)
        self.reg_entry = self._create_input(form, "Reg ID:", 1)

        # Actions
        tk.Button(self, text="Generate & Save to DB", bg="#28a745", fg="white", 
                  font=("Arial", 12), command=self.handle_registration).pack(pady=10)

        self.download_btn = tk.Button(self, text="Download QR Image", bg="#17a2b8", fg="white",
                                      state="disabled", command=self.download_qr)
        self.download_btn.pack(pady=5)

        self.qr_preview = tk.Label(self, text="QR Preview", bg="#f8f9fa", width=20, height=10)
        self.qr_preview.pack(pady=10)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), 
                  bg="#6c757d", fg="white").pack(pady=20)

    def _create_input(self, parent, label, row):
        tk.Label(parent, text=label, bg="#ffffff").grid(row=row, column=0, sticky="w")
        entry = tk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def handle_registration(self):
        name, reg_id = self.name_entry.get().strip(), self.reg_entry.get().strip()
        if not name or not reg_id:
            return messagebox.showwarning("Error", "Fields cannot be empty")

        qr_hash, file_path = self.generator.create_qr(reg_id, name)
        if self.db.add_student(reg_id, name, qr_hash):
            self.last_generated_path = file_path
            self.download_btn.config(state="normal")
            self._display_qr(file_path)
            messagebox.showinfo("Success", "Registered!")
        else:
            messagebox.showerror("Error", "ID already exists")

    def download_qr(self):
        if not self.last_generated_path: return
        target = filedialog.asksaveasfilename(defaultextension=".png", 
                                              initialfile=os.path.basename(self.last_generated_path))
        if target:
            shutil.copy(self.last_generated_path, target)
            messagebox.showinfo("Success", "QR Saved!")

    # ui/qr_page.py (Updated Fix)
    def _display_qr(self, path):
        """Ensures the QR image is formatted and visible in the UI."""
        img = Image.open(path)
        # Use a high-quality resampling for better visibility
        img = img.resize((220, 220), Image.Resampling.LANCZOS) 
        img_tk = ImageTk.PhotoImage(img)
        
        # Clear placeholder text and apply image
        self.qr_preview.config(image=img_tk, text="", width=220, height=220)
        self.qr_preview.image = img_tk # Mandatory reference to prevent garbage collection