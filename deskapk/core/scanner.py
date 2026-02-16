# core/scanner.py
import cv2
import logging
try:
    from pyzbar import pyzbar
except ImportError:
    pyzbar = None

class QRScanner:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cap = None
        self.is_running = False

    def start_camera(self):
        """Attempts to open the camera with fallback indices."""
        # Try index 0 (default), then 1 (external), then -1
        for idx in [0, 1, -1]:
            self.cap = cv2.VideoCapture(idx)
            if self.cap.isOpened():
                # Warm up the camera by reading a test frame
                ret, _ = self.cap.read()
                if ret:
                    self.is_running = True
                    return True
                self.cap.release()
        return False

    def stop_camera(self):
        if self.cap:
            self.cap.release()
        self.cap = None
        self.is_running = False

    def process_frame(self):
        if not self.is_running or self.cap is None:
            return None, "Camera Offline", None

        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None, "Error: No Feed Received", None

        status_msg = "Scanner Active"
        student_name = None

        if pyzbar is None:
            return frame, "Dependency Error: pyzbar missing", None

        # QR Detection
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            qr_hash = obj.data.decode('utf-8')
            student = self.db_manager.get_student_by_hash(qr_hash)
            
            if student:
                reg_id, name = student
                student_name = name
                result = self.db_manager.mark_attendance(reg_id)
                status_msg = f"Success: {name}" if result == "SUCCESS" else f"Notice: {name} already marked"
                color = (0, 255, 0) if result == "SUCCESS" else (0, 165, 255)
            else:
                status_msg = "Unknown QR Code"
                color = (0, 0, 255)

            # Draw Feedback
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            cv2.putText(frame, status_msg, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame, status_msg, student_name