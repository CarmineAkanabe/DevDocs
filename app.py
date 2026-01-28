#!/usr/bin/env python3
"""
DevDocs - Offline Documentation Reader for Developers
A desktop application to download, store, and read documentation offline.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
import tkinter as tk
import time


def main():
    """Run the application with an aesthetic splash screen."""
    # Create transient splash using tkinter for minimal dependency during startup
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.attributes('-topmost', True)

    w = 560
    h = 220
    ws = splash.winfo_screenwidth()
    hs = splash.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    splash.geometry(f"{w}x{h}+{x}+{y}")

    # Background frame
    frame = tk.Frame(splash, bg="#081018")
    frame.pack(fill="both", expand=True)

    title = tk.Label(frame, text="DevDocs", fg="#22aa44", bg="#081018", font=("Segoe UI", 28, "bold"))
    title.pack(pady=(28, 4))

    subtitle = tk.Label(frame, text="Offline Documentation Reader", fg="#cfeee0", bg="#081018", font=("Segoe UI", 12))
    subtitle.pack()

    # Decorative separator
    sep = tk.Frame(frame, height=2, bg="#0f3f1f")
    sep.pack(fill="x", padx=60, pady=12)

    # Progress bar simulation
    progress_frame = tk.Frame(frame, bg="#081018")
    progress_frame.pack(fill="x", padx=60)
    canvas = tk.Canvas(progress_frame, width=440, height=10, bg="#0b0e12", highlightthickness=0)
    canvas.pack()
    bar = canvas.create_rectangle(0, 0, 0, 10, fill="#22aa44", width=0)

    splash.update()

    # Animate progress bar quickly for polish
    for i in range(0, 441, 22):
        canvas.coords(bar, 0, 0, i, 10)
        splash.update()
        time.sleep(0.03)

    # Pause briefly then destroy splash
    splash.after(300, splash.destroy)
    splash.mainloop()

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
