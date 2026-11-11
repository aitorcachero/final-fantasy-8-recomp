@echo off
title Final Fantasy VIII Recompiled - Preparador Universal de Disco (CDs 1 a 4)
cd /d "%~dp0"
echo ========================================================
echo   Iniciando Preparador de Discos de Final Fantasy VIII
echo ========================================================
echo.
py -3 "tools\setup_disc.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error preparando los discos.
    pause
) else (
    echo.
    echo Todo listo. Ya puedes hacer doble clic en JUGAR_FINAL_FANTASY_VIII.bat
    pause
)
