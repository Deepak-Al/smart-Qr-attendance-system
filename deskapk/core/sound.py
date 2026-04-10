import win32com.client

import pythoncom

class NameCall:
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        pythoncom.CoInitialize()

    def name_call(self,name):
        self.speaker.Speak(f"{name} is present.")
        pythoncom.CoUninitialize()

    def call_notice(self,name):
        self.speaker.Speak(f"{name} already marked.")
        pythoncom.CoUninitialize()

    def invalid_qr(self):
        self.speaker.Speak("Invalid QR")
        pythoncom.CoUninitialize()