import os
import sys
import subprocess

def install_dependencies():
    """Check and install missing dependencies automatically."""
    required = ["google-genai", "python-dotenv", "fpdf2", "pillow", "requests"]
    for lib in required:
        try:
            if lib == "google-genai":
                import google.genai
            elif lib == "python-dotenv":
                import dotenv
            elif lib == "fpdf2":
                import fpdf
            elif lib == "pillow":
                import PIL
            elif lib == "requests":
                import requests
        except ImportError:
            print(f"[*] Missing {lib}. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Run installer before importing nexus modules
install_dependencies()

from nexus.ui.main_window import MainWindow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Ensure projects directory exists
    if not os.path.exists("projects"):
        os.makedirs("projects")
        
    # Start the Ultimate Nexus God Writer
    app = MainWindow()
    app.mainloop()
