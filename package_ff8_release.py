import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(r"G:\Proyectos\decomp-ps1")
FF8_DIR = BASE_DIR / "final-fantasy-8-recomp"
RELEASES_DIR = BASE_DIR / "releases"
REL_FOLDER = RELEASES_DIR / "Final_Fantasy_VIII_Recompiled_v1.0_Release"
ZIP_PATH = RELEASES_DIR / "Final_Fantasy_VIII_Recompiled_v1.0_Windows_x64.zip"

def create_release():
    print(f"[*] Limpiando y preparando directorio de release: {REL_FOLDER}")
    if REL_FOLDER.exists():
        shutil.rmtree(REL_FOLDER)
    REL_FOLDER.mkdir(parents=True, exist_ok=True)
    (REL_FOLDER / "disc").mkdir(parents=True, exist_ok=True)
    (REL_FOLDER / "saves").mkdir(parents=True, exist_ok=True)
    (REL_FOLDER / "tools").mkdir(parents=True, exist_ok=True)
    (REL_FOLDER / "bios").mkdir(parents=True, exist_ok=True)

    # Copiar BIOS
    if (FF8_DIR / "build-release" / "bios" / "openbios.bin").exists():
        shutil.copy2(FF8_DIR / "build-release" / "bios" / "openbios.bin", REL_FOLDER / "bios" / "openbios.bin")
    elif (BASE_DIR / "bios" / "openbios.bin").exists():
        shutil.copy2(BASE_DIR / "bios" / "openbios.bin", REL_FOLDER / "bios" / "openbios.bin")

    # Copiar keybinds e input si existen
    for ini in ["keybinds.ini", "input.ini"]:
        if (FF8_DIR / "build-release" / ini).exists():
            shutil.copy2(FF8_DIR / "build-release" / ini, REL_FOLDER / ini)
        elif (FF8_DIR / ini).exists():
            shutil.copy2(FF8_DIR / ini, REL_FOLDER / ini)

    # 1. Copiar ejecutables
    if (FF8_DIR / "Final_Fantasy_VIII_Launcher.exe").exists():
        shutil.copy2(FF8_DIR / "Final_Fantasy_VIII_Launcher.exe", REL_FOLDER / "Final_Fantasy_VIII_Launcher.exe")
    shutil.copy2(FF8_DIR / "FinalFantasy8.exe", REL_FOLDER / "FinalFantasy8.exe")
    shutil.copy2(FF8_DIR / "build-release" / "Final_Fantasy_VIII_Recompiled.exe", REL_FOLDER / "Final_Fantasy_VIII_Recompiled.exe")

    # 2. Copiar configuracion
    shutil.copy2(FF8_DIR / "game.toml", REL_FOLDER / "game.toml")
    if (FF8_DIR / "settings.toml").exists():
        shutil.copy2(FF8_DIR / "settings.toml", REL_FOLDER / "settings.toml")

    # 3. Copiar scripts por lotes
    bat_files = [
        "JUGAR_FINAL_FANTASY_VIII.bat",
        "JUGAR_FINAL_FANTASY_VIII_4K_43.bat",
        "JUGAR_FINAL_FANTASY_VIII_21_9_ULTRAWIDE.bat",
        "CONFIGURAR_FINAL_FANTASY_VIII.bat",
        "PREPARAR_DISCO.bat"
    ]
    for b in bat_files:
        src = FF8_DIR / b
        if src.exists():
            shutil.copy2(src, REL_FOLDER / b)

    # 4. Copiar herramientas
    if (FF8_DIR / "tools" / "chdman.exe").exists():
        shutil.copy2(FF8_DIR / "tools" / "chdman.exe", REL_FOLDER / "tools" / "chdman.exe")
    if (FF8_DIR / "tools" / "setup_disc.py").exists():
        shutil.copy2(FF8_DIR / "tools" / "setup_disc.py", REL_FOLDER / "tools" / "setup_disc.py")

    # 5. Disc README
    disc_readme = (
        "Coloca aqui tus imagenes originales de Final Fantasy VIII (Discos 1 al 4) en formato .CHD o .BIN/.CUE.\n"
        "Luego ejecuta PREPARAR_DISCO.bat para desempaquetarlos automaticamente si son .CHD.\n"
    )
    with open(REL_FOLDER / "disc" / "COPIA_TUS_DISCOS_AQUI.txt", "w", encoding="utf-8") as f:
        f.write(disc_readme)

    # 6. LEEME_INSTRUCCIONES.txt
    leeme_text = """================================================================================
  FINAL FANTASY VIII RECOMPILED (4K 60FPS 16:9 / 21:9 MASTER EDITION)
  Port Nativo para PC (Windows x64) - Square Soft
================================================================================

¡Bienvenido a la remasterizacion definitiva de Final Fantasy VIII en PC!

CARACTERISTICAS DE ESTA VERSION:
- Port Nativo 64-bit compilado directamente a codigo maquina C / LLVM Clang.
- Resolucion interna 4K UHD nativa con Supersampling (SSAA 2.0x).
- Soporte completo para los 4 CDs con selector de disco integrado y deteccion instantanea.
- PGXP Geometry Correction: Elimina el temblor (jitter / polygon wobble) poligonal
  en personajes, escenarios 3D, mapa del mundo y arenas de combate.
- Perspective Texturing y Depth Buffer de 32-bit con antialiasing FXAA HQ.
- Escalado bicubic y suavizado de croma para todas las cinematicas CGI (FMVs).
- Audio SPU HQ con interpolacion Gaussiana a 48kHz sin distorsion.
- Formato panoramico 16:9 y soporte 21:9 Ultrawide con HUD y menus protegidos.
- Compatibilidad nativa con mandos DualShock / Xbox / PlayStation / Teclado.
- 100% Legal y libre de derechos de autor (no incluye ISOs comerciales).

--------------------------------------------------------------------------------
COMO JUGAR EN 3 SIMPLES PASOS:
--------------------------------------------------------------------------------

1. Copia tus imagenes de Final Fantasy VIII (Discos 1 al 4) en formato .CHD o
   .BIN/.CUE dentro de la carpeta 'disc\\'.
   
2. Si estan en .CHD, haz doble clic en 'PREPARAR_DISCO.bat' para descomprimirlos
   en unos segundos.

3. ¡Listo! Para jugar tienes varias opciones:
   - 'FinalFantasy8.exe' : Lanzador silencioso directo en 4K 16:9.
   - 'JUGAR_FINAL_FANTASY_VIII.bat' : Lanzador 16:9 Widescreen 4K 60FPS.
   - 'JUGAR_FINAL_FANTASY_VIII_21_9_ULTRAWIDE.bat' : Modo 21:9 Ultra-Panoramico.
   - 'JUGAR_FINAL_FANTASY_VIII_4K_43.bat' : Modo 4:3 Clasico original.
   - 'CONFIGURAR_FINAL_FANTASY_VIII.bat' : Abre el menu de ajustes graficos, mandos y mods.

--------------------------------------------------------------------------------
CONTROLES POR DEFECTO:
--------------------------------------------------------------------------------
- Mandos Xbox / PlayStation (DualShock Analogico):
  * Stick izquierdo / Cruceta : Movimiento de Squall y navegacion en menus
  * Boton A / Cruz : Confirmar / Interactuar / Hablar
  * Boton B / Circulo : Cancelar / Salir de menu
  * Boton X / Cuadrado : Menu de juego / Triple Triad (cartas)
  * Boton Y / Triangulo : Gatillo de Gunblade (disparo critico en combate)
  * L1 / R1 : Huir de batalla / Cambiar objetivo
  * Start : Pausa
  * Select : Mapa del mundo / Ayuda

================================================================================
"""
    with open(REL_FOLDER / "LEEME_INSTRUCCIONES.txt", "w", encoding="utf-8") as f:
        f.write(leeme_text)

    readme_md = """# Final Fantasy VIII Recompiled (Windows x64)

Port nativo para PC de **Final Fantasy VIII** (Square Soft, 1999) mediante recompilación estática MIPS R3000A a C nativo con Clang/LLVM.

## Mejoras incluidas:
- **Resolución 4K Ultra HD** con supersampling 2.0x.
- **Soporte completo de 4 CDs** con cambio de disco dinámico.
- **PGXP Subpixel Precision**: supresión de temblor poligonal en personajes, mapamundi y combates.
- **Perspective-Correct Texturing**: texturas con mapeo en perspectiva sin distorsión.
- **Filtro Bicúbico para FMVs**: cinematicas CGI renderizadas a máxima calidad de croma.
- **SPU HQ Audio**: mezcla de 24 canales con interpolación Gaussiana y búfer de baja latencia.
- **Aspect Ratio 16:9 y 21:9 Ultrawide**: campo de visión panorámico ampliado.
- **Controles Analógicos**: soporte directo para mandos modernos (XInput, DualShock, DirectInput).
"""
    with open(REL_FOLDER / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_md)

    print(f"[*] Creando archivo ZIP: {ZIP_PATH}...")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(REL_FOLDER):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(RELEASES_DIR)
                zipf.write(file_path, arcname)

    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    print(f"[OK] Paquete completado con exito: {ZIP_PATH} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_release()
