from ui.app import App
import os

def initialize_folders():
    """Ensures all required system folders exist before startup."""
    folders = ['database', 'assets/qrcodes', 'exports']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created system folder: {folder}")

if __name__ == "__main__":
    # 1. Prepare environment
    initialize_folders()
    
    # 2. Launch Application
    print("Starting Smart QR Attendance System...")
    app = App()
    app.mainloop()



    """
    
    """