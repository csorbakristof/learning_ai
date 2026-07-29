@echo off
cd /d "%~dp0"
echo Compiling ImageQuantizer.java...
javac -source 8 -target 8 ImageQuantizer.java
if %ERRORLEVEL% EQU 0 (
    echo Compilation successful!
    echo You can now run the application with: java ImageQuantizer
) else (
    echo Compilation failed!
)
pause
