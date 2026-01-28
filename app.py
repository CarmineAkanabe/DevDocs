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


def main():
    """Run the application."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
