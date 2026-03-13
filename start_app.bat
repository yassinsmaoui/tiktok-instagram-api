@echo off
echo Demarrage de l'application...
echo.

start "FastAPI Server" cmd /k "cd /d %~dp0 && venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

start "Streamlit App" cmd /k "cd /d %~dp0 && venv\Scripts\streamlit.exe run streamlit_app.py"

echo.
echo FastAPI: http://localhost:8000
echo Streamlit: http://localhost:8501
echo.
