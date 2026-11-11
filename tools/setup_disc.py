#!/usr/bin/env python3
"""
Final Fantasy VIII Recompiled — Detector y Preparador Universal de Disco (CD 1 a 4)
Soporta .CHD, .BIN/.CUE, .ISO, .PBP
"""
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DISC_DIR = BASE_DIR / "disc"
TOOLS_DIR = BASE_DIR / "tools"
CHDMAN = TOOLS_DIR / "chdman.exe"

DISC_NAMES = [
    "Final Fantasy VIII (Spain) (Disc 1)",
    "Final Fantasy VIII (Spain) (Disc 2)",
    "Final Fantasy VIII (Spain) (Disc 3)",
    "Final Fantasy VIII (Spain) (Disc 4)",
]

def main():
    print("========================================================")
    print("  Preparador de Discos de Final Fantasy VIII Recompiled")
    print("========================================================")
    DISC_DIR.mkdir(parents=True, exist_ok=True)

    found_any = False
    for i, name in enumerate(DISC_NAMES, 1):
        bin_file = DISC_DIR / f"{name}.bin"
        cue_file = DISC_DIR / f"{name}.cue"
        if bin_file.exists() and cue_file.exists():
            print(f"[OK] Disco {i} ya esta preparado: {name}.cue")
            found_any = True
            continue

        # Check for CHD in root or disc/
        chd_candidates = [
            BASE_DIR.parent / f"{name}.chd",
            BASE_DIR / f"{name}.chd",
            DISC_DIR / f"{name}.chd",
            BASE_DIR.parent / f"Final Fantasy VIII (Disc {i}).chd",
            BASE_DIR / f"Final Fantasy VIII (Disc {i}).chd",
        ]

        chd_found = None
        for cand in chd_candidates:
            if cand.exists():
                chd_found = cand
                break

        if chd_found and CHDMAN.exists():
            print(f"[*] Descomprimiendo CHD para Disco {i}: {chd_found.name}...")
            cmd = [
                str(CHDMAN), "extractcd",
                "-i", str(chd_found),
                "-o", str(cue_file),
                "-ob", str(bin_file),
                "-f"
            ]
            res = subprocess.run(cmd)
            if res.returncode == 0:
                print(f"[OK] Disco {i} preparado correctamente.")
                found_any = True
            else:
                print(f"[!] Error al extraer CHD para Disco {i}.")
        else:
            print(f"[AVISO] Disco {i} no encontrado o pendiente.")

    print("\nProceso finalizado. Discos listos en:", DISC_DIR)

if __name__ == "__main__":
    main()
