import asyncio
import pathlib
from fastmcp import FastMCP, Image
# pip install pywin32 mss
import win32gui
import mss
# pip install Pillow
import PIL.Image
# pip install opencv-python
import cv2

# pip install pyttsx3
import pyttsx3
import tkinter as tk
from tkinter import simpledialog

import io
import os
import time

# Create an MCP server
mcp = FastMCP("HumanMCP",
              description="Monitor, control and manage human via through the Model Context Protocol(MCP)")

# 画像をキャプチャする
@mcp.tool()
def human_screen_capture(resizeRatio:float=0.25) -> Image:
    """Monitor what the human is doing in PC screen."""

    with mss.mss() as sct:
        # 全画面キャプチャ
        monitor = sct.monitors[0]  # 全画面のモニター情報を取得
        screenshot = sct.grab(monitor)
        # mssのScreenShotオブジェクトをPillowのImageオブジェクトに変換
        img = PIL.Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        new_size = (int(img.width * resizeRatio), int(img.height * resizeRatio)) # 幅と高さを50%にリサイズ
        img_resized = img.resize(new_size, PIL.Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        img_resized.save(buffer, format='PNG', optimize=True, compress_level=9)
        # Reset the buffer position to the beginning
        buffer.seek(0)
        # Return an Image object with the data and format of the buffer
        return Image(data=buffer.getvalue(), format="png")

@mcp.tool()
def human_webcam_capture() -> Image:
    """Monitor the human facial expressions with a webcam."""

    # Open the webcam
    cap = cv2.VideoCapture(0)
    # Read a frame from the webcam
    ret, frame = cap.read()
    # Release the webcam
    cap.release()
    # Convert the frame to a PIL Image
    img = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', optimize=True, compress_level=9)
    # Reset the buffer position to the beginning
    buffer.seek(0)
    # Return an Image object with the data and format of the buffer
    return Image(data=buffer.getvalue(), format="png")

@mcp.tool()
def get_current_datetime() -> str:
    """Get the current date and time."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

@mcp.tool()
async def wait_and_get_current_datetime(seconds:int=180) -> str:
    """Wait for a specified number of seconds. This function returns an inaccurate second. So return the current date and time strings."""
    if seconds > 180:
        await asyncio.sleep(180)
        return get_current_datetime()
    else:
        await asyncio.sleep(seconds)
        return  get_current_datetime()
    
@mcp.tool()
def speak(text:str) -> bool:
    """Speak a text string using the text-to-speech engine. The human can hear it."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return True

@mcp.tool()
def show_askstring_dialog(title:str, message:str) -> str|None:
    """Show a dialog box to ask a string input from the human."""
    speak(f"ダイアログに入力してください。{message}")
    root = tk.Tk()
    root.withdraw()
    # 文字入力ダイアログを表示
    user_input:str|None = simpledialog.askstring(title, message)
    root.destroy()
    return user_input

@mcp.tool()
def write_humanmcp_memory(content: str) -> bool:
    """
    Write the specified content to 'streamermcp_memory.txt'.
    Overwrites any existing content.
    """
    memo_path = pathlib.Path.cwd() / "humanmcp_memory.txt"
    with open(memo_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

@mcp.tool()
def read_humanmcp_memory() -> str:
    """
    Read and return the content of 'streamermcp_memory.txt'.
    Returns an empty string if the file does not exist.
    """
    memo_path = pathlib.Path.cwd() / "humanmcp_memory.txt"
    if memo_path.exists():
        with open(memo_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""
if __name__ == "__main__":
    mcp.run(transport="stdio")