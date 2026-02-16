import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="database/attendance.db"):
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_tables()

    def _get_connection(self):
        """Returns a connection to the database."""
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """Initializes the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Students Table: Stores primary info and unique QR hash
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    reg_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    qr_hash TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Attendance Logs: Stores every scan with date/time
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reg_id TEXT NOT NULL,
                    scan_date DATE NOT NULL,
                    scan_time TIME NOT NULL,
                    FOREIGN KEY (reg_id) REFERENCES students (reg_id)
                )
            ''')
            conn.commit()

    # --- Student Management ---

    def add_student(self, reg_id, name, qr_hash):
        """Registers a new student. Returns True if successful."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (reg_id, name, qr_hash) VALUES (?, ?, ?)",
                    (reg_id, name, qr_hash)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Reg ID or Hash already exists

    def get_student_by_hash(self, qr_hash):
        """Retrieves student details using the scanned QR hash."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT reg_id, name FROM students WHERE qr_hash = ?", (qr_hash,))
            return cursor.fetchone()

    # --- Attendance Logic ---

    def mark_attendance(self, reg_id):
        """
        Logs attendance for a student. 
        Includes a logic-gate to prevent multiple scans on the same day.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M:%S")

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Check if already scanned today
            cursor.execute(
                "SELECT id FROM attendance WHERE reg_id = ? AND scan_date = ?", 
                (reg_id, today)
            )
            if cursor.fetchone():
                return "ALREADY_MARKED"

            # Record new attendance
            cursor.execute(
                "INSERT INTO attendance (reg_id, scan_date, scan_time) VALUES (?, ?, ?)",
                (reg_id, today, now_time)
            )
            conn.commit()
            return "SUCCESS"

    # --- Analytics & Reporting ---

    def get_daily_stats(self):
        """Returns total present count for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT reg_id) FROM attendance WHERE scan_date = ?", (today,))
            return cursor.fetchone()[0]

    def get_all_attendance_data(self):
        """Retrieves a joined report for Excel export."""
        query = '''
            SELECT s.reg_id, s.name, a.scan_date, a.scan_time 
            FROM students s
            LEFT JOIN attendance a ON s.reg_id = a.reg_id
            ORDER BY a.scan_date DESC, a.scan_time DESC
        '''
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

      
        
    def delete_attendance(self, reg_id, scan_date):
        """
        Removes a specific attendance record.
        This is used to correct errors or remove fraudulent scans.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # We use both reg_id and scan_date to ensure we delete the correct record
                cursor.execute(
                    "DELETE FROM attendance WHERE reg_id = ? AND scan_date = ?", 
                    (reg_id, scan_date)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Database Error during deletion: {e}")
            return False
        

    def get_all_students(self):
        """Retrieves all registered students for management."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT reg_id, name, created_at FROM students ORDER BY name ASC")
            return cursor.fetchall()

    def update_student(self, reg_id, new_name):
        """Updates a student's name in the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET name = ? WHERE reg_id = ?", (new_name, reg_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Update Error: {e}")
            return False

    def delete_student(self, reg_id):
        """Permanently removes a student and their attendance history."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # 1. Delete attendance records first (Foreign Key requirement)
                cursor.execute("DELETE FROM attendance WHERE reg_id = ?", (reg_id,))
                # 2. Delete student profile
                cursor.execute("DELETE FROM students WHERE reg_id = ?", (reg_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Deletion Error: {e}")
            return False