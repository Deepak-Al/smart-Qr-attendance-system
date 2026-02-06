import tkinter as tk

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Attendance Dashboard", font=("Arial", 20)).pack(pady=20)

        # Camera placeholder
        camera_frame = tk.LabelFrame(self, text="Camera Feed", width=400, height=300)
        camera_frame.pack(pady=10)

        # Attendance stats
        stats_frame = tk.LabelFrame(self, text="Statistics")
        stats_frame.pack(pady=10)

        tk.Label(stats_frame, text="Total Students: 0").pack()
        tk.Label(stats_frame, text="Present: 0").pack()
        tk.Label(stats_frame, text="Absent: 0").pack()

        tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame("HomePage")
        ).pack(pady=20)
