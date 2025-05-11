@echo off
REM Step 1: Create virtual environment
python -m venv myvenv
call myvenv\Scripts\activate

REM Step 2: Install dependencies
pip install pyinstaller

REM Step 3: Build EXE
pyinstaller --noconsole --onefile --name "NEOExplorer" neo_explorer.py

REM Step 4: Move EXE to root
move dist\NEOExplorer.exe .

REM Cleanup
rmdir /s /q build
rmdir /s /q dist
del NEOExplorer.spec

echo Build completed! Check for NEOExplorer.exe
pause