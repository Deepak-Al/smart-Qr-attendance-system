import pandas as pd
import os
from datetime import datetime

class AttendanceExporter:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        # Ensure the exports directory exists
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_to_excel(self, data):
        """
        Converts database records into a formatted Excel file.
        Input 'data' is a list of tuples: (reg_id, name, date, time)
        """
        if not data:
            return None, "No data available to export."

        # 1. Convert to a Pandas DataFrame
        columns = ["Registration ID", "Student Name", "Date", "Time"]
        df = pd.DataFrame(data, columns=columns)

        # 2. Generate a professional filename with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Attendance_Report_{timestamp}.xlsx"
        file_path = os.path.join(self.export_dir, filename)

        try:
            writer = pd.ExcelWriter(file_path, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name='Attendance Logs')
            worksheet = writer.sheets['Attendance Logs']
            
            for idx, col in enumerate(df.columns):
                # SAFE LENGTH CALCULATION: 
                # Convert every value to string before checking length to avoid 'float' errors
                series_max = df[col].apply(lambda x: len(str(x)) if x is not None else 0).max()
                max_len = max(series_max, len(str(col))) + 4
                worksheet.column_dimensions[chr(65 + idx)].width = max_len
                
            writer.close()
            return file_path, "Success"
        except Exception as e:
            return None, f"Export Error: {str(e)}"