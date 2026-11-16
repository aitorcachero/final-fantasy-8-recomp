#!/usr/bin/env python3
"""
Final Fantasy VIII Recompiled — Detector y Preparador Universal de Disco (CD 1 a 4)
Soporta .CHD, .BIN/.CUE, .ISO, .PBP
"""
import os
import sys
import subprocess
import argparse
import re
import shutil
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

def import_disc(i, src):
    """Pone el disco i (.cue o .chd del jugador) en disc/ con el nombre que usa el juego."""
    name = DISC_NAMES[i - 1]
    src = Path(src).expanduser().resolve()
    if not src.is_file():
        raise RuntimeError(f"Disco {i}: no se encuentra el archivo {src}")
    DISC_DIR.mkdir(parents=True, exist_ok=True)
    cue_file = DISC_DIR / f"{name}.cue"
    ext = src.suffix.lower()
    if ext == ".chd":
        if not CHDMAN.exists():
            raise RuntimeError("Falta tools/chdman.exe para descomprimir el CHD")
        res = subprocess.run(
            [str(CHDMAN), "extractcd", "-i", str(src), "-o", str(cue_file),
             "-ob", str(DISC_DIR / f"{name}.bin"), "-f"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            raise RuntimeError(f"Disco {i}: error al extraer el CHD {src.name}")
    elif ext == ".cue":
        text = src.read_text(encoding="utf-8", errors="replace")
        refs = re.findall(r'FILE\s+"([^"]+)"', text)
        if not refs:
            raise RuntimeError(f"Disco {i}: el .cue {src.name} no indica ningun .bin")
        for n, ref in enumerate(refs, 1):
            bin_src = src.parent / ref
            if not bin_src.is_file():
                raise RuntimeError(f"Disco {i}: falta el archivo {ref} del .cue")
            dest_name = f"{name}.bin" if len(refs) == 1 else f"{name} (Track {n}).bin"
            dest = DISC_DIR / dest_name
            if bin_src.resolve() != dest.resolve():
                shutil.copy2(bin_src, dest)
            text = text.replace(f'"{ref}"', f'"{dest_name}"', 1)
        cue_file.write_text(text, encoding="utf-8")
    else:
        raise RuntimeError(f"Disco {i}: se esperaba un .cue o un .chd, no {src.suffix}")

def cli():
    parser = argparse.ArgumentParser(description="Preparador de discos de Final Fantasy VIII Recompiled")
    parser.add_argument("--prepare", action="store_true", help="modo sin ventana, con lineas de progreso")
    parser.add_argument("--game", help="disco 1 (.cue o .chd)")
    parser.add_argument("--disc2", help="disco 2 (.cue o .chd)")
    parser.add_argument("--disc3", help="disco 3 (.cue o .chd)")
    parser.add_argument("--disc4", help="disco 4 (.cue o .chd)")
    args = parser.parse_args()
    discs = [(i, p) for i, p in ((1, args.game), (2, args.disc2), (3, args.disc3), (4, args.disc4)) if p]
    if not args.prepare and not discs:
        main()
        return 0
    if not args.game:
        print("Falta --game <disco 1: .cue o .chd>", file=sys.stderr)
        return 1
    try:
        for done, (i, p) in enumerate(discs):
            print(f"progress {done / len(discs):.2f} Preparando disco {i}", flush=True)
            import_disc(i, p)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    print("progress 1.0 Discos listos", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(cli())
