@echo off

cd /d %~dp0

python auto_creat_sidebar.py
python reWrite-README-file.py

rem timeout /nobreak /t 5

pause