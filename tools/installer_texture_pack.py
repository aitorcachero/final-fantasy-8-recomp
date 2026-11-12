#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Fantasy VIII Recompiled — Asistente Automatizado de Instalación de Texturas HD
Permite arrastrar cualquier archivo comprimido (.zip, .rar, .7z) o carpeta de texturas
y lo instala automáticamente en la estructura de SLES-02084 activando el mod en state.toml.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

GAME_ID = "SLES-02084"

def find_project_root():
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "Final_Fantasy_VIII_Recompiled.exe").exists() or (candidate / "game.toml").exists():
        return candidate
    if (candidate / "build-release" / "Final_Fantasy_VIII_Recompiled.exe").exists():
        return candidate
    return Path.cwd()

def ensure_state_enabled(root_dir: Path):
    mods_dir = root_dir / "mods"
    mods_dir.mkdir(parents=True, exist_ok=True)
    state_file = mods_dir / "state.toml"
    content = f"""format_version = 2

[[package]]
id = "psx.enhancement.hd-textures"
version = "1.0.0"

[[feature]]
package_id = "psx.enhancement.hd-textures"
id = "hd-textures"
enabled = true

[feature.values]
replacements = "true"
dump = "false"

[feature.resources]
pack = "mods/texture-packs/{GAME_ID}"
"""
    state_file.write_text(content, encoding="utf-8")
    print(f"[OK] Inyeccion de texturas HD activada en mods/state.toml")

def extract_archive(archive_path: Path, temp_dir: Path) -> bool:
    print(f"[*] Descomprimiendo: {archive_path.name}...")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Si es .zip estándar
    if archive_path.suffix.lower() == ".zip":
        try:
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(temp_dir)
            return True
        except Exception as e:
            print(f"[!] Error extrayendo zip con Python ({e}), probando con tar...")

    # 2. Intentar con tar (nativo en Windows 10/11)
    res = subprocess.run(["tar", "-xf", str(archive_path), "-C", str(temp_dir)], capture_output=True)
    if res.returncode == 0:
        return True

    # 3. Intentar con PowerShell Expand-Archive
    if archive_path.suffix.lower() == ".zip":
        ps_cmd = f"Expand-Archive -Path '{archive_path}' -DestinationPath '{temp_dir}' -Force"
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
        return res.returncode == 0

    return False

def install_textures(source_dir: Path, target_dir: Path) -> int:
    target_dir.mkdir(parents=True, exist_ok=True)
    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    count = 0

    # Buscar si hay una subcarpeta 'replacements'
    rep_dirs = [p for p in source_dir.rglob("replacements") if p.is_dir()]
    search_root = rep_dirs[0] if rep_dirs else source_dir

    # Si hay carpetas con nombres de serial (ej: SLUS-00892)
    serials = [p for p in source_dir.rglob("SLUS-*") if p.is_dir()]
    if serials and not rep_dirs:
        search_root = serials[0]
        if (search_root / "replacements").is_dir():
            search_root = search_root / "replacements"

    print(f"[*] Buscando imágenes HD en: {search_root.name}...")

    for root, _, files in os.walk(search_root):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in valid_exts:
                dest = target_dir / f
                # Si no existe o se sobreescribe
                shutil.copy2(p, dest)
                count += 1

    return count

def main():
    root_dir = find_project_root()
    target_dir = root_dir / "mods" / "texture-packs" / GAME_ID / "replacements"
    if (root_dir / "build-release" / "mods").exists():
        target_dir = root_dir / "build-release" / "mods" / "texture-packs" / GAME_ID / "replacements"

    print("=" * 72)
    print("  FINAL FANTASY VIII RECOMPILED — INSTALADOR AUTOMATIZADO DE TEXTURAS HD")
    print("=" * 72)

    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1]).resolve()
    else:
        print("\nArrastra aquí tu archivo comprimido (.zip / .rar / .7z) o la carpeta")
        print("donde tengas el pack de texturas y presiona Enter:")
        val = input("> ").strip().strip('"').strip("'")
        if not val:
            print("[!] Operación cancelada.")
            return
        input_path = Path(val).resolve()

    if not input_path.exists():
        print(f"[ERROR] No se encuentra la ruta indicada: {input_path}")
        return

    temp_dir = root_dir / ".temp_pack_extract"
    is_archive = input_path.is_file() and input_path.suffix.lower() in {".zip", ".rar", ".7z", ".tar", ".gz"}

    try:
        if is_archive:
            if not extract_archive(input_path, temp_dir):
                print(f"[ERROR] No se pudo descomprimir el archivo: {input_path}")
                print("Por favor, descomprímelo manualmente y arrastra la carpeta resultante.")
                return
            source_folder = temp_dir
        else:
            source_folder = input_path

        total = install_textures(source_folder, target_dir)
        ensure_state_enabled(root_dir)
        if (root_dir / "build-release").exists():
            ensure_state_enabled(root_dir / "build-release")

        print("\n" + "=" * 72)
        print(f" [¡EXITO!] Se han instalado {total} texturas HD correctamente.")
        print(f" Carpeta de texturas: {target_dir}")
        print(" El pack ya esta activo y listo para jugar.")
        print("=" * 72 + "\n")

    finally:
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

if __name__ == "__main__":
    main()
