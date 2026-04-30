@echo off
setlocal enabledelayedexpansion

echo ========================================
echo NUST HELP BOT - Complete Launcher
echo ========================================
echo.

cd /d "%~dp0"

REM Check if portable Python exists
set "PYTHON_CMD=portable_python\python.exe"
if not exist "%PYTHON_CMD%" (
    echo Portable Python not found. Installing...
    echo This will be contained within the project folder only.
    echo.
    
    REM Download portable Python
    echo Downloading portable Python...
    curl -L -o "python-3.11.9-embed-amd64.zip" "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
    
    if errorlevel 1 (
        echo ERROR: Failed to download Python
        echo Please check your internet connection
        pause
        exit /b 1
    )
    
    REM Extract portable Python
    echo Extracting portable Python...
    powershell -Command "Expand-Archive -Path 'python-3.11.9-embed-amd64.zip' -DestinationPath 'portable_python' -Force"
    
    if errorlevel 1 (
        echo ERROR: Failed to extract Python
        pause
        exit /b 1
    )
    
    REM Configure portable Python
    echo Configuring portable Python...
    echo python311.zip > portable_python\python311._pth
    echo . >> portable_python\python311._pth
    echo Lib\site-packages >> portable_python\python311._pth
    
    REM Download and install pip
    echo Installing pip...
    curl -L -o "get-pip.py" "https://bootstrap.pypa.io/get-pip.py"
    portable_python\python.exe get-pip.py --no-warn-script-location
    
    REM Clean up
    del python-3.11.9-embed-amd64.zip
    del get-pip.py
    
    echo Portable Python installation completed!
    echo.
) else (
    echo Portable Python found!
)

REM Install all required packages
echo Installing required packages (this may take several minutes)...
echo This includes: Streamlit, LangChain, ChromaDB, Transformers, etc.
"%PYTHON_CMD%" -m pip install streamlit pyinstaller requests langchain langchain-community langchain-chroma langchain-ollama langchain-nomic chromadb pypdf transformers torch sentencepiece numpy pandas nomic --no-warn-script-location
echo All packages installed!

REM Check if Ollama is installed
echo Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo OLLAMA NOT FOUND!
    echo Please install Ollama from: https://ollama.com/download
    echo Then run this batch file again.
    pause
    exit /b 1
) else (
    echo Ollama is already installed!
)

REM Check if Ollama is running
echo Checking Ollama server...
ollama list >nul 2>&1
if errorlevel 1 (
    echo Starting Ollama server...
    start "Ollama Server" ollama serve
    echo Waiting for server to start...
    timeout /t 15 /nobreak >nul
)


REM Check DeepSeek model
echo Checking DeepSeek model...
ollama list | findstr deepseek-r1:1.5b >nul
if errorlevel 1 (
    echo Downloading DeepSeek model...
    ollama pull deepseek-r1:1.5b
)

REM Check Nomic embedding model
echo Checking Nomic embedding model...
ollama list | findstr nomic-embed-text >nul
if errorlevel 1 (
    echo Downloading Nomic embedding model...
    ollama pull nomic-embed-text
)

echo.
echo ========================================
echo Starting NUST Help Bot
echo ========================================
echo.
echo Server will start at: http://localhost:8501
echo.
echo IMPORTANT: Keep this window open to keep the server running!
echo Close this window to stop the application.
echo.

REM Start the application
"%PYTHON_CMD%" -m streamlit run app.py --server.port 8501

pause
