@echo off
cd dist
cls
pydoc -w lib_Net
cd ..
move .\dist\*.html .\
exit
