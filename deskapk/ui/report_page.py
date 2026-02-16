import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.db_manager import DatabaseManager
from core.exporter import AttendanceExporter

class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller
        self.db = DatabaseManager()
        self.exporter = AttendanceExporter()

        # --- HEADER ---
        header = tk.Frame(self, bg="#343a40", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Management & Reports", font=("Arial", 16, "bold"), 
                 bg="#343a40", fg="white").pack(side="left", padx=20, pady=15)

        self.count_banner = tk.Label(header, text="Records: 0", font=("Arial", 12), bg="#343a40", fg="#28a745")
        self.count_banner.pack(side="right", padx=20)

        # --- TABBED INTERFACE ---
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill="both", padx=20, pady=10)

        # Tab 1: Attendance Logs
        self.attendance_tab = tk.Frame(self.tabs, bg="#f4f6f9")
        self.tabs.add(self.attendance_tab, text=" Attendance Logs ")
        self._build_attendance_tab()

        # Tab 2: Student Management
        self.student_tab = tk.Frame(self.tabs, bg="#f4f6f9")
        self.tabs.add(self.student_tab, text=" Manage Students ")
        self._build_student_tab()

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"),
                  bg="#6c757d", fg="white", width=15).pack(pady=10)

    def _build_search_bar(self, parent, callback):
        """Standard search bar component for both tabs."""
        search_frame = tk.Frame(parent, bg="#f4f6f9")
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="🔍 Search:", bg="#f4f6f9").pack(side="left", padx=5)
        entry = tk.Entry(search_frame, width=30)
        entry.pack(side="left", padx=5)
        entry.bind("<KeyRelease>", lambda e: callback(entry.get()))
        return entry

    def _build_attendance_tab(self):
        container = tk.Frame(self.attendance_tab, bg="#f4f6f9", padx=10, pady=10)
        container.pack(expand=True, fill="both")

        # Search, Refresh & Export Row
        top_row = tk.Frame(container, bg="#f4f6f9")
        top_row.pack(fill="x")
        
        # Search Bar
        self._build_search_bar(top_row, self.filter_attendance)
        
        # RESTORED: Refresh Button
        tk.Button(top_row, text="🔄 Refresh", bg="#17a2b8", fg="white", 
                command=self.load_data, width=12).pack(side="left", padx=10)
        
        # Export Button
        tk.Button(top_row, text="📊 Export to Excel", bg="#28a745", fg="white", 
                command=self.handle_export).pack(side="right", padx=5)

        # Table
        self.tree = ttk.Treeview(container, columns=("ID", "Name", "Date", "Time"), show='headings')
        for col in ("ID", "Name", "Date", "Time"): self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", pady=10)

        # Right-click Delete
        self.att_menu = tk.Menu(self, tearoff=0)
        self.att_menu.add_command(label="❌ Delete Record", command=self.confirm_delete_attendance)
        self.tree.bind("<Button-3>", lambda e: self._show_menu(e, self.tree, self.att_menu))
        
        self.load_data()

    def _build_student_tab(self):
        container = tk.Frame(self.student_tab, bg="#f4f6f9", padx=10, pady=10)
        container.pack(expand=True, fill="both")

        # Top Row for Students
        top_row = tk.Frame(container, bg="#f4f6f9")
        top_row.pack(fill="x")
        
        self._build_search_bar(top_row, self.filter_students)
        
        # RESTORED: Refresh Button for Students
        tk.Button(top_row, text="🔄 Refresh List", bg="#17a2b8", fg="white", 
                command=self.load_students, width=15).pack(side="left", padx=10)

        self.student_tree = ttk.Treeview(container, columns=("ID", "Name", "Joined"), show='headings')
        for col in ("ID", "Name", "Joined"): self.student_tree.heading(col, text=col)
        self.student_tree.pack(expand=True, fill="both", pady=10)

        # Right-click Edit/Delete
        self.std_menu = tk.Menu(self, tearoff=0)
        self.std_menu.add_command(label="✏️ Edit Name", command=self.edit_student)
        self.std_menu.add_command(label="🗑️ Delete Student", command=self.remove_student_profile)
        self.student_tree.bind("<Button-3>", lambda e: self._show_menu(e, self.student_tree, self.std_menu))

        self.load_students()

    # --- LOGIC & FILTERING ---

    def filter_attendance(self, query):
        query = query.lower()
        self.load_data(query)

    def filter_students(self, query):
        query = query.lower()
        self.load_students(query)

    def load_data(self, filter_q=""):
        for i in self.tree.get_children(): self.tree.delete(i)
        records = self.db.get_all_attendance_data()
        self.count_banner.config(text=f"Records Found: {len(records)}")
        for r in records:
            if filter_q in str(r[0]).lower() or filter_q in str(r[1]).lower():
                self.tree.insert("", tk.END, values=r)

    def load_students(self, filter_q=""):
        for i in self.student_tree.get_children(): self.student_tree.delete(i)
        students = self.db.get_all_students()
        for s in students:
            if filter_q in str(s[0]).lower() or filter_q in str(s[1]).lower():
                self.student_tree.insert("", tk.END, values=s)

    def _show_menu(self, event, tree, menu):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            menu.post(event.x_root, event.y_root)

    def confirm_delete_attendance(self):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0])['values']
            if messagebox.askyesno("Delete", f"Remove record for {v[1]}?"):
                self.db.delete_attendance(v[0], v[2])
                self.load_data()

    def edit_student(self):
        sel = self.student_tree.selection()
        if sel:
            v = self.student_tree.item(sel[0])['values']
            new_name = simpledialog.askstring("Edit", f"New name for {v[0]}:", initialvalue=v[1])
            if new_name:
                self.db.update_student(v[0], new_name)
                self.load_students()
                self.load_data()

    def remove_student_profile(self):
        sel = self.student_tree.selection()
        if sel:
            v = self.student_tree.item(sel[0])['values']
            if messagebox.askyesno("Warning", f"Delete {v[1]} and all their logs?"):
                self.db.delete_student(v[0])
                self.load_students()
                self.load_data()

    def handle_export(self):
        data = self.db.get_all_attendance_data()
        path, status = self.exporter.export_to_excel(data)
        if path: messagebox.showinfo("Success", f"Saved to {path}")
        else: messagebox.showerror("Error", status)