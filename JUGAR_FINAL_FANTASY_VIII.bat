@echo off
cd /d "%~dp0"
title Final Fantasy VIII Recompiled - Launcher Master Edition

:: 1. Lanzador grafico moderno estilo SNES Recomp (con selector de 4 CDs y mejoras de todo tipo)
if exist "Final_Fantasy_VIII_Launcher.exe" (
    start "" "Final_Fantasy_VIII_Launcher.exe" %*
    exit /b
)
if exist "build-release\Final_Fantasy_VIII_Launcher.exe" (
    start "" "build-release\Final_Fantasy_VIII_Launcher.exe" %*
    exit /b
)

:: 2. Lanzador Python directo si aplica
if exist "launcher_ff8.py" (
    start "" py -3 "launcher_ff8.py" %*
    exit /b
)

:: 3. Lanzador nativo directo C
if exist "FinalFantasy8.exe" (
    start "" "FinalFantasy8.exe" %*
    exit /b
)

:: 4. Ejecutable en build-release
if exist "build-release\Final_Fantasy_VIII_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Final_Fantasy_VIII_Recompiled.exe" %*
    exit /b
)

echo [ERROR] No se encontro el ejecutable o lanzador de Final Fantasy VIII.
pause
exit /b
