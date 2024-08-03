import subprocess
import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)
    # Speak the text
    engine.say(text)
    engine.runAndWait()

def launch_calculator():
    # Launch the system calculator
    subprocess.Popen('calc', shell=True)
    speak("Calculator launched")

if __name__ == "__main__":
    launch_calculator()
