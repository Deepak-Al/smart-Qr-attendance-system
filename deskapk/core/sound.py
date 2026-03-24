import pyttsx3

class NameCall:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id) # try 0 / 1
        self.engine.setProperty('rate', 150) # speed
        self.engine.setProperty('volume', 1.0)

    def name_call(self,name):
        self.engine.say(f"{name} is present.")
        self.engine.runAndWait()

    def call_notice(self,name):
        self.engine.say(f"{name} already marked.")
        self.engine.runAndWait()

    def invalid_qr(self):
        self.engine.say("Invalid QR.")
        self.engine.runAndWait()