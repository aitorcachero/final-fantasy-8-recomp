@echo off
cd /d "%~dp0"
title Final Fantasy VIII - Pantalla de Inicio y Configuracion de Mejoras

if exist "Final_Fantasy_VIII_Launcher.exe" (
    start "" "Final_Fantasy_VIII_Launcher.exe"
    exit /b
)
if exist "build-release\Final_Fantasy_VIII_Launcher.exe" (
    start "" "build-release\Final_Fantasy_VIII_Launcher.exe"
    exit /b
)
if exist "launcher_ff8.py" (
    start "" py -3 "launcher_ff8.py"
    exit /b
)
if exist "build-release\Final_Fantasy_VIII_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Final_Fantasy_VIII_Recompiled.exe" --launcher
    exit /b
)
if exist "FinalFantasy8.exe" (
    start "" "FinalFantasy8.exe" --launcher
    exit /b
)

echo [ERROR] No se encontro el lanzador de Final Fantasy VIII.
pause
exit /b
