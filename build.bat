pyinstaller --onefile --noconsole  --hidden-import=tkinter --hidden-import=pyautogui --hidden-import=Pillow --hidden-import=win32gui --hidden-import=win32con  --icon=SILENT\image\icon_all_sizes.ico SILENT\src\SILENT.py

REM Specify your dedicated env
REM .venv\Scripts\python -m pyinstaller --onefile --noconsole  --hidden-import=tkinter --hidden-import=pyautogui --hidden-import=Pillow --hidden-import=win32gui --hidden-import=win32con  --icon=SILENT\image\icon_all_sizes.ico SILENT\src\SILENT.py
