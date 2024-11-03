import pynput
from pynput.keyboard import Key, Controller
import time
keyboard = Controller()

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def type_line(text):
    for char in text:
        press_key(char)  # Press each character
        time.sleep(0.05)  # Add a small delay between keystrokes (optional)

# Example usage:
type_line("Hello, world!") # Types out "Hello, world!"
#press_key(Key.enter)  # Presses the Enter key