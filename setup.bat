@echo off
echo ==========================================
echo   NEXUS GOD WRITER - AUTO SETUP
echo ==========================================
echo.
echo [1/2] Installing Python Dependencies...
pip install google-genai python-dotenv pillow markdown fpdf2
echo.
echo [2/2] Checking for .env file...
if not exist .env (
    echo GEMINI_API_KEY=your_api_key_here > .env
    echo Created .env file. Please open it and add your Gemini API Key.
) else (
    echo .env file already exists.
)
echo.
echo ==========================================
echo   SETUP COMPLETE! 
echo   You can now run the app with: python main.py
echo ==========================================
pause
