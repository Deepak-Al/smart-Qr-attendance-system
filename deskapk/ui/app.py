import tkinter as tk
from ui.home_page import HomePage
from ui.qr_page import QRPage
from ui.dashboard_page import DashboardPage
from ui.report_page import ReportPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart QR Attendance System v1.0")
        self.geometry("1100x700") # Increased default size
        self.resizable(True, True) # ALLOW FULL SCREEN
        self.configure(bg="#f4f6f9")

        # Main container for pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize all pages
        for Page in (HomePage, QRPage, DashboardPage, ReportPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()