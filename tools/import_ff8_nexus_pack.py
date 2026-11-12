#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Fantasy VIII Recompiled — Importador de Paquetes de Texturas HD
Permite integrar paquetes de texturas HD de DuckStation y adaptar packs
comunitarios (como el HD Pack de Nexus / ESRGAN) a la estructura del runtime.
"""

import os
import sys
import shutil
from pathlib import Path

GAME_ID = "SLES-02084"

def get_target_replacements_dir(base_dir: Path) -> Path:
    candidates = [
        base_dir / "mods" / "texture-packs" / GAME_ID / "replacements",
        base_dir / "build-release" / "mods" / "texture-packs" / GAME_ID / "replacements",
        base_dir.parent / "mods" / "texture-packs" / GAME_ID / "replacements",
    ]
    for c in candidates:
        if c.parent.exists():
            c.mkdir(parents=True, exist_ok=True)
            return c
    # Por defecto
    target = base_dir / "mods" / "texture-packs" / GAME_ID / "replacements"
    target.mkdir(parents=True, exist_ok=True)
    return target

def import_texture_pack(source_dir: Path, target_dir: Path):
    if not source_dir.exists():
        print(f"[ERROR] La carpeta de origen no existe: {source_dir}")
        return False

    print(f"[*] Analizando archivos en: {source_dir}")
    print(f"[*] Carpeta destino: {target_dir}")

    # Extensiones de imagen soportadas por psxrecomp
    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    imported = 0
    skipped = 0

    for root, _, files in os.walk(source_dir):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in valid_exts:
                # Mantener estructura relativa o copiar directamente
                rel = p.relative_to(source_dir)
                dest = target_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
                imported += 1
            else:
                skipped += 1

    print(f"\n[OK] Importación completada:")
    print(f"  - Imágenes HD importadas: {imported}")
    if skipped > 0:
        print(f"  - Archivos omitidos (no imagen): {skipped}")
    print(f"\nLas texturas están listas en:\n{target_dir}\n")
    print("Asegúrate de tener activada la opción 'Habilitar Texturas y Fondos HD' en el launcher.")
    return True

def main():
    base_dir = Path(__file__).resolve().parent.parent
    target_dir = get_target_replacements_dir(base_dir)

    print("=" * 70)
    print("FINAL FANTASY VIII RECOMPILED — ASISTENTE DE TEXTURAS HD")
    print("=" * 70)
    print(f"Directorio de instalación de texturas: {target_dir}\n")

    if len(sys.argv) > 1:
        source_path = Path(sys.argv[1]).resolve()
    else:
        print("Indica la ruta de la carpeta donde has descomprimido el mod o pack HD:")
        path_str = input("> ").strip().strip('"').strip("'")
        if not path_str:
            print("Operación cancelada.")
            return
        source_path = Path(path_str).resolve()

    import_texture_pack(source_path, target_dir)

if __name__ == "__main__":
    main()
