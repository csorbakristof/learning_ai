@echo off
cd /d "%~dp0"
echo Compiling and starting Image Quantizer...
javac -source 8 -target 8 ImageQuantizer.java
if %ERRORLEVEL% EQU 0 (
    echo Starting application...
    java ImageQuantizer
) else (
    echo Compilation failed!
    pause
)
