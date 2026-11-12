@echo off
cd /d "%~dp0"
title Final Fantasy VIII Recompiled - 16:9 Panoramico Pantalla Completa

:: Modo Panoramico 16:9 que llena todo el monitor sin distorsiones
set PSX_RENDER_THREAD=0
set PSX_PRESENT_THREAD=0
set PSX_FRAME_GEN=0
set PSX_FRAME_INTERPOLATION=0
set PSX_VSYNC=0
set PSX_FPS_TELEMETRY=0
set PSX_FREEZE_HEARTBEAT=0
set PSX_ASPECT_RATIO=16:9
set PSX_INTERNAL_SCALE=8

if exist "FinalFantasy8.exe" (
    start "" "FinalFantasy8.exe" %*
    exit /b
)
if exist "build-release\FinalFantasy8.exe" (
    start "" "build-release\FinalFantasy8.exe" %*
    exit /b
)
if exist "build-release\Final_Fantasy_VIII_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Final_Fantasy_VIII_Recompiled.exe" %*
    exit /b
)
if exist "Final_Fantasy_VIII_Recompiled.exe" (
    start "" "Final_Fantasy_VIII_Recompiled.exe" %*
    exit /b
)

echo [ERROR] No se encontro el ejecutable de Final Fantasy VIII Recompiled.
pause
exit /b
