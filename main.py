from nexus.ui.main_window import MainWindow
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Ensure projects directory exists
    if not os.path.exists("projects"):
        os.makedirs("projects")
        
    app = MainWindow()
    app.mainloop()
