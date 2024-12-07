@echo off
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Running app.py...
python app.py
pause
