import os
import sys
import subprocess

def install_dependencies():
    """Check and install missing dependencies automatically."""
    required = ["google-generativeai", "python-dotenv", "fpdf2", "pillow"]
    for lib in required:
        try:
            if lib == "google-generativeai":
                import google.generativeai
            elif lib == "python-dotenv":
                import dotenv
            elif lib == "fpdf2":
                import fpdf
            elif lib == "pillow":
                import PIL
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
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Critical Error: {e}")
