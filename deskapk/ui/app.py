import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart QR Attendance System")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Container for all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        from ui.home_page import HomePage
        from ui.qr_page import QRPage
        from ui.dashboard_page import DashboardPage
        from ui.report_page import ReportPage

        for Page in (HomePage, QRPage, DashboardPage, ReportPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
