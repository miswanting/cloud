@echo off
del *.log
cls
call test.py
cd ..
move /Y dist\*.log .\
pause
