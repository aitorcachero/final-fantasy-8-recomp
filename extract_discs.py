import subprocess
import os
import sys

root = r"G:\Proyectos\decomp-ps1"
chdman = os.path.join(root, "tools", "chdman.exe")
disc_dir = os.path.join(root, "final-fantasy-8-recomp", "disc")

discs = [
    ("Final Fantasy VIII (Spain) (Disc 2).chd", "Final Fantasy VIII (Spain) (Disc 2).cue", "Final Fantasy VIII (Spain) (Disc 2).bin"),
    ("Final Fantasy VIII (Spain) (Disc 3).chd", "Final Fantasy VIII (Spain) (Disc 3).cue", "Final Fantasy VIII (Spain) (Disc 3).bin"),
    ("Final Fantasy VIII (Spain) (Disc 4).chd", "Final Fantasy VIII (Spain) (Disc 4).cue", "Final Fantasy VIII (Spain) (Disc 4).bin"),
]

for chd_name, cue_name, bin_name in discs:
    chd_path = os.path.join(root, chd_name)
    cue_path = os.path.join(disc_dir, cue_name)
    bin_path = os.path.join(disc_dir, bin_name)
    
    if os.path.exists(cue_path) and os.path.exists(bin_path):
        print(f"Skipping {cue_name}, already extracted.")
        continue
        
    print(f"Extracting {chd_name} -> {cue_name}...")
    cmd = [chdman, "extractcd", "-i", chd_path, "-o", cue_path, "-ob", bin_path]
    subprocess.run(cmd, check=True)
    print(f"Done extracting {cue_name}.")

print("All discs extracted successfully!")
