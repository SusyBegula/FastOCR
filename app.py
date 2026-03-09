from evdev import InputDevice, categorize, ecodes
import subprocess
import cv2
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import subprocess

load_dotenv() 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
device = InputDevice('/dev/input/event2')
pressed_keys = set()

def capture_screenshot():
    region = subprocess.check_output(["slurp"]).decode().strip()
    subprocess.run(["grim", "-g", region, "snip.png"])
    get_text()


def get_text():
    try:
        with open("snip.png", "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Extract all text from this image exactly as it appears.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/png",
                ),
            ],
        )

        text = response.text

        # copy to clipboard
        subprocess.run(["wl-copy"], input=text.encode())

        # success notification
        subprocess.run([
            "notify-send",
            "-u", "normal",
            "-t", "2000",
            "-i", "dialog-information",
            "FastOCR",
            "OCR completed successfully"
        ])

    except Exception as e:
        # error notification
        subprocess.run([
            "notify-send",
            "-u", "critical",
            "-t", "4000",
            "-i", "dialog-error",
            "FastOCR Error",
            str(e)
        ])

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        key = key_event.scancode

        if key_event.keystate == key_event.key_down:
            pressed_keys.add(key)

        elif key_event.keystate == key_event.key_up:
            pressed_keys.discard(key)

        if (ecodes.KEY_LEFTCTRL in pressed_keys or ecodes.KEY_RIGHTCTRL in pressed_keys) and ecodes.KEY_SYSRQ in pressed_keys:
            # print("Ctrl + Print Screen pressed")
            capture_screenshot()
