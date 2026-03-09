# FastOCR

FastOCR is a lightweight **screen-snipping OCR tool for Linux (Wayland / Hyprland)** that lets you quickly extract text from any region of your screen and automatically copy it to the clipboard.

It works similarly to **Windows PowerToys Text Extractor**, but is built with Python and integrates with Wayland tools.

## Features

* Select any screen region to extract text
* Automatically copies recognized text to clipboard
* Desktop notifications for success or errors
* Works on **Wayland / Hyprland**
* Uses **Google Gemini** for high-quality OCR
* Global hotkey trigger

## Demo Workflow

Press the hotkey:

```
Ctrl + PrintScreen
```

Then:

1. Select a region of the screen
2. Screenshot is captured
3. Text is extracted using Gemini
4. Text is copied to clipboard
5. Notification appears

Pipeline:

```
Hotkey → slurp → grim → Gemini OCR → wl-copy
```

## Requirements

Linux with Wayland (tested on **Hyprland**)

Required system tools:

```
slurp
grim
wl-clipboard
libnotify
```

Install them:

```bash
sudo pacman -S grim slurp wl-clipboard libnotify
```

## Python Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

Get an API key from Google AI Studio.

## Running the Program

Run:

```bash
python main.py
```

Then press:

```
Ctrl + PrintScreen
```

Select a region and OCR will run automatically.

## Notifications

FastOCR sends desktop notifications using `notify-send`.

Success:

```
OCR completed successfully
```

Failure:

```
FastOCR Error
```

## How It Works

The program listens to keyboard events using `evdev` and waits for:

```
Ctrl + PrintScreen
```

When triggered:

1. `slurp` lets you select a screen region
2. `grim` captures the screenshot
3. The screenshot is sent to Gemini Vision
4. Extracted text is copied to clipboard using `wl-copy`
5. A notification is displayed

## Project Structure

```
FastOCR/
│
├── main.py
├── snip.png
├── .env
└── README.md
```
