import qrcode
import hashlib
import os
from PIL import Image

class QRGenerator:
    def __init__(self, output_dir="assets/qrcodes"):
        self.output_dir = output_dir
        # Ensure the output directory exists for saving images
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_student_hash(self, reg_id, name):
        """
        Creates a unique, secure hash for the student.
        This hash will be the actual content of the QR code.
        """
        raw_data = f"{reg_id}:{name}:smart_qr_secret_2024"
        return hashlib.sha256(raw_data.encode()).hexdigest()[:16]

    def create_qr(self, reg_id, name):
        """
        Generates a QR code image, saves it, and returns the hash and file path.
        """
        # 1. Generate the secure hash
        qr_hash = self.generate_student_hash(reg_id, name)
        
        # 2. Setup QR Code parameters
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_hash)
        qr.make(fit=True)

        # 3. Create the image (using a professional color scheme)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 4. Save the file with a clear naming convention
        filename = f"{reg_id}_{name.replace(' ', '_')}.png"
        file_path = os.path.join(self.output_dir, filename)
        img.save(file_path)

        return qr_hash, file_path

    def get_qr_path(self, reg_id, name):
        """Helper to find an existing QR code path."""
        filename = f"{reg_id}_{name.replace(' ', '_')}.png"
        return os.path.join(self.output_dir, filename)