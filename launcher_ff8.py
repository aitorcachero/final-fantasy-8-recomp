#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Fantasy VIII Recompiled — Master Launcher
Estilo visual moderno inspirado en Sega Rally Revo / Terranigma SNES Recomp.
Paleta Dark Slate Navy + Vibrant Orange. Lanzamiento directo sin ventanas intermedias.
"""

import os
import sys
import subprocess
import ctypes
from pathlib import Path
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# ── Colores Sega Rally Revo / Terranigma Recomp ──
C_BG_DEEP       = "#090d16"   # Fondo ventana principal
C_CARD_BG       = "#101827"   # Tarjetas Slate Navy
C_CARD_HOVER    = "#162238"   # Tarjeta iluminada al pasar ratón
C_BORDER        = "#202e48"   # Borde azul pizarra suave
C_ORANGE        = "#ff6600"   # Naranja vibrante Sega Rally
C_ORANGE_HOVER  = "#ff7e26"   # Naranja hover
C_ORANGE_DARK   = "#d95300"   # Naranja presionado
C_TEXT_WHITE    = "#f8fafc"   # Texto blanco
C_TEXT_MUTED    = "#94a3b8"   # Texto secundario
C_CYAN          = "#38bdf8"   # Cian brillante para acentos
C_GREEN         = "#22c55e"   # Verde estado OK

# ── Detección de ruta absoluta del ejecutable y entorno ──
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

def find_game_environment():
    """Localiza el ejecutable recompilado y el directorio de trabajo correcto"""
    candidates = [
        # 1. Mismo directorio del lanzador (release estándar)
        (BASE_DIR / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR),
        # 2. En build-release
        (BASE_DIR / "build-release" / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR / "build-release"),
        # 3. Subcarpeta final-fantasy-8-recomp
        (BASE_DIR / "final-fantasy-8-recomp" / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR / "final-fantasy-8-recomp"),
        (BASE_DIR / "final-fantasy-8-recomp" / "build-release" / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR / "final-fantasy-8-recomp" / "build-release"),
        # 4. Carpeta padre
        (BASE_DIR.parent / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR.parent),
        (BASE_DIR.parent / "build-release" / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR.parent / "build-release"),
        (BASE_DIR.parent / "final-fantasy-8-recomp" / "build-release" / "Final_Fantasy_VIII_Recompiled.exe", BASE_DIR.parent / "final-fantasy-8-recomp" / "build-release"),
    ]
    for exe, work_dir in candidates:
        if exe.exists():
            return exe.resolve(), work_dir.resolve()
    if (BASE_DIR / "build-release").exists():
        return (BASE_DIR / "build-release" / "Final_Fantasy_VIII_Recompiled.exe").resolve(), (BASE_DIR / "build-release").resolve()
    return (BASE_DIR / "Final_Fantasy_VIII_Recompiled.exe").resolve(), BASE_DIR.resolve()

GAME_EXE, GAME_WORK_DIR = find_game_environment()

DISCS_INFO = [
    {
        "id": 1,
        "title": "DISCO 1: Misión SeeD & Timber",
        "cue": "disc/Final Fantasy VIII (Spain) (Disc 1).cue",
        "desc": "El examen en Dollet, graduación en Balamb, el baile con Rinoa y la emboscada a la delegación de Galbadia."
    },
    {
        "id": 2,
        "title": "DISCO 2: Balamb Móvil & Edea",
        "cue": "disc/Final Fantasy VIII (Spain) (Disc 2).cue",
        "desc": "El jardín móvil de Balamb, la prisión del desierto, el conflicto entre jardines y el combate contra Edea."
    },
    {
        "id": 3,
        "title": "DISCO 3: Estación Espacial & Esthar",
        "cue": "disc/Final Fantasy VIII (Spain) (Disc 3).cue",
        "desc": "El viaje a Esthar, la estación espacial en órbita, el rescate de Rinoa y el despertar de Lunatic Pandora."
    },
    {
        "id": 4,
        "title": "DISCO 4: Compresión Temporal",
        "cue": "disc/Final Fantasy VIII (Spain) (Disc 4).cue",
        "desc": "La compresión del espacio-tiempo, el castillo de Artemisa y la batalla final por el destino del universo."
    }
]

def detect_gamepad_name():
    """Detecta el nombre del mando conectado"""
    try:
        xinput = ctypes.windll.xinput1_4
        class XINPUT_STATE(ctypes.Structure):
            _fields_ = [("dwPacketNumber", ctypes.c_ulong), ("Gamepad", ctypes.c_ubyte * 12)]
        for i in range(4):
            state = XINPUT_STATE()
            if xinput.XInputGetState(i, ctypes.byref(state)) == 0:
                return f"Mando Xbox / XInput (Puerto {i+1}) [Conectado]"
    except Exception:
        pass

    try:
        num_devs = ctypes.windll.winmm.joyGetNumDevs()
        if num_devs > 0:
            return "Mando USB / DirectInput [Conectado]"
    except Exception:
        pass

    return "Teclado / Sin mando detectado"

def parse_toml(path: Path) -> dict:
    data = {}
    cur = "root"
    if not path.exists():
        return data
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith("#"): continue
                if l.startswith("[") and l.endswith("]"):
                    cur = l[1:-1].strip()
                    if cur not in data: data[cur] = {}
                    continue
                if "=" in l:
                    k, v = l.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if cur not in data: data[cur] = {}
                    data[cur][k] = v
    except Exception:
        pass
    return data

def save_mod_state(work_dir: Path, hd_textures_enabled: bool, dump_enabled: bool):
    for base in [work_dir, BASE_DIR]:
        try:
            mods_dir = base / "mods"
            mods_dir.mkdir(parents=True, exist_ok=True)
            tex_pack_dir = mods_dir / "texture-packs" / "SLES-02084"
            (tex_pack_dir / "replacements").mkdir(parents=True, exist_ok=True)
            (tex_pack_dir / "dumps").mkdir(parents=True, exist_ok=True)

            state_file = mods_dir / "state.toml"
            if hd_textures_enabled or dump_enabled:
                content = f"""format_version = 2

[[package]]
id = "psx.enhancement.hd-textures"
version = "1.0.0"

[[feature]]
package_id = "psx.enhancement.hd-textures"
id = "hd-textures"
enabled = true

[feature.values]
replacements = "{"true" if hd_textures_enabled else "false"}"
dump = "{"true" if dump_enabled else "false"}"

[feature.resources]
pack = "mods/texture-packs/SLES-02084"
"""
            else:
                content = "format_version = 2\n"
            state_file.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"Error escribiendo mods/state.toml: {e}")

def save_game_settings(settings: dict):
    exe, work_dir = find_game_environment()
    work_dir.mkdir(parents=True, exist_ok=True)
    post_shader_val = "shaders/remaster_cinematic.pfx" if settings.get("remaster_shader", True) else ""
    bloom_val = "0.40" if settings.get("hdr_bloom", True) else "0.0"
    aa_val = "fxaa_hq" if settings.get("fxaa_hq", True) else "off"

    content = f"""# psxrecomp user settings - written by Sega Rally Revo / Terranigma style launcher.
[video]
renderer          = "opengl"
window_width      = {settings.get('window_width', 1920)}
fast_boot         = false
bios_hle          = true
fullscreen        = {1 if settings.get('fullscreen', False) else 0}
render_thread     = false
present_thread    = false
frame_generation  = false
vsync             = "{settings.get('vsync', 'off')}"
frame_interpolation = false
frame_interpolation_fps = 0
aspect_ratio      = "{settings.get('aspect_ratio', '16:9')}"
supersample       = 2.0
antialiasing_mode = "{aa_val}"
bloom             = {bloom_val}
post_shader       = "{post_shader_val}"
texture_filtering = "bilinear"
fmv_filter        = "bicubic"
fmv_chroma_smoothing = true
geometry_correction = {str(settings.get('pgxp_geometry', True)).lower()}
perspective_texturing = {str(settings.get('pgxp_perspective', True)).lower()}

[hotkeys]
rewind_pad = 1272
save_state_menu_pad = 2040
fast_forward_speed = {settings.get('fast_forward_speed', 4)}
fast_forward_mode = "hold"
fast_forward_pad = 1528
fast_forward_toggle_pad = 0

[launcher]
skip_launcher = true
freeze_heartbeat = false

[disc]
path = "{settings.get('disc_path', 'disc/Final Fantasy VIII (Spain) (Disc 1).cue')}"
selected = {settings.get('disc_selected', 1)}

[memcard]
dir     = "saves"
card1   = "saves/card1.mcd"
card2   = "saves/card2.mcd"
enable1 = true
enable2 = true

[controller]
p1_device = "0300fa675e040000130b000023057801"
p1_mode   = "{settings.get('p1_mode', 'analog')}"
p1_deadzone = {settings.get('deadzone', 3276)}
multitap  = true
multitap_analog = true
deadzone  = {settings.get('deadzone', 3276)}

[localization]
language = "es"

[enhancements]
turbo_loads = {str(settings.get('turbo_loads', True)).lower()}
auto_skip_fmv = {str(settings.get('auto_skip_fmv', False)).lower()}
pgxp_geometry = {str(settings.get('pgxp_geometry', True)).lower()}
pgxp_perspective = {str(settings.get('pgxp_perspective', True)).lower()}
bicubic_fmv = {str(settings.get('bicubic_fmv', True)).lower()}
spu_hq = {str(settings.get('spu_hq', True)).lower()}
gunblade_perfect = {str(settings.get('gunblade_perfect', False)).lower()}
no_encounters = {str(settings.get('no_encounters', False)).lower()}
ap_boost = {settings.get('ap_boost', 1)}
max_gil = {str(settings.get('max_gil', False)).lower()}
"""
    try:
        with open(work_dir / "settings.toml", "w", encoding="utf-8") as f:
            f.write(content)
        if BASE_DIR != work_dir:
            with open(BASE_DIR / "settings.toml", "w", encoding="utf-8") as f:
                f.write(content)
        save_mod_state(work_dir, settings.get("hd_textures", True), settings.get("dump_textures", False))
    except Exception as e:
        print(f"Error escribiendo settings.toml: {e}")

class FF8ModernLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Final Fantasy VIII — Recompiled PC Edition")
        self.geometry("1020x680")
        self.minsize(940, 620)
        self.configure(fg_color=C_BG_DEEP)

        ctk.set_appearance_mode("Dark")

        # Cargar valores previos
        exe, work_dir = find_game_environment()
        s_path = work_dir / "settings.toml"
        if not s_path.exists() and (BASE_DIR / "settings.toml").exists():
            s_path = BASE_DIR / "settings.toml"
        prev = parse_toml(s_path)

        disc_prev = int(prev.get("disc", {}).get("selected", 1))
        self.var_disc = tk.IntVar(value=disc_prev)

        self.var_preset = tk.StringVar(value="4K 60FPS Widescreen")
        self.var_resolution = tk.StringVar(value="4K Ultra HD (3840x2160 - 8x SSAA)")
        self.var_aspect = tk.StringVar(value="16:9 Panorámico")
        self.var_fullscreen = tk.BooleanVar(value=prev.get("video", {}).get("fullscreen", "0") == "1")
        self.var_vsync = tk.StringVar(value="Desactivado (Baja latencia)")
        self.var_tex_filter = tk.StringVar(value="Bilineal + Anisotrópico 16x")

        # Pipeline Remaster Nativo
        vid = prev.get("video", {})
        self.var_remaster_shader = tk.BooleanVar(value=vid.get("post_shader", "shaders/remaster_cinematic.pfx") != "")
        self.var_hdr_bloom = tk.BooleanVar(value=float(vid.get("bloom", "0.40")) > 0.05)
        self.var_fxaa_hq = tk.BooleanVar(value=vid.get("antialiasing_mode", "fxaa_hq") != "off")

        # Mejoras
        enh = prev.get("enhancements", {})
        self.var_pgxp = tk.BooleanVar(value=enh.get("pgxp_geometry", "true") == "true")
        self.var_perspective = tk.BooleanVar(value=enh.get("pgxp_perspective", "true") == "true")
        self.var_turbo_loads = tk.BooleanVar(value=enh.get("turbo_loads", "true") == "true")
        self.var_bicubic_fmv = tk.BooleanVar(value=enh.get("bicubic_fmv", "true") == "true")
        self.var_spu_hq = tk.BooleanVar(value=enh.get("spu_hq", "true") == "true")
        self.var_skip_fmv = tk.BooleanVar(value=enh.get("auto_skip_fmv", "false") == "true")
        self.var_ff_speed = tk.StringVar(value="4x")

        # QoL / Cheats
        self.var_gunblade = tk.BooleanVar(value=enh.get("gunblade_perfect", "false") == "true")
        self.var_no_encounters = tk.BooleanVar(value=enh.get("no_encounters", "false") == "true")
        self.var_ap_boost = tk.StringVar(value="Normal (1x)")
        self.var_max_gil = tk.BooleanVar(value=enh.get("max_gil", "false") == "true")

        # Texturas HD (mods/state.toml)
        hd_tex_enabled = True
        dump_tex_enabled = False
        state_file = work_dir / "mods" / "state.toml"
        if not state_file.exists() and (BASE_DIR / "mods" / "state.toml").exists():
            state_file = BASE_DIR / "mods" / "state.toml"
        if state_file.exists():
            try:
                txt = state_file.read_text(encoding="utf-8")
                hd_tex_enabled = "psx.enhancement.hd-textures" in txt and 'replacements = "true"' in txt
                dump_tex_enabled = 'dump = "true"' in txt
            except Exception:
                pass
        self.var_hd_textures = tk.BooleanVar(value=hd_tex_enabled)
        self.var_dump_textures = tk.BooleanVar(value=dump_tex_enabled)

        # Mandos
        ctrl = prev.get("controller", {})
        self.var_pad_mode = tk.StringVar(value="DualShock Analógico (Sticks Activos)" if ctrl.get("p1_mode", "analog") == "analog" else "Digital Clásico (Cruceta)")
        self.var_deadzone = tk.IntVar(value=int(ctrl.get("deadzone", 3276)))
        self.var_rumble = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        # ── Contenedor principal horizontal: Columna Izquierda (Branding/CDs) + Derecha (Pestañas) ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=(15, 10))

        # ── Panel Izquierdo (290px): Título, Póster y Selector de Discos ──
        left_panel = ctk.CTkFrame(body, width=290, fg_color=C_CARD_BG, corner_radius=12, border_width=1, border_color=C_BORDER)
        left_panel.pack(side="left", fill="y", padx=(0, 15))
        left_panel.pack_propagate(False)

        # Encabezado izquierdo
        head_box = ctk.CTkFrame(left_panel, fg_color="transparent")
        head_box.pack(fill="x", padx=16, pady=(18, 12))

        ctk.CTkLabel(head_box, text="FINAL FANTASY VIII", font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=C_TEXT_WHITE).pack(anchor="w")
        ctk.CTkLabel(head_box, text="RECOMPILED PC EDITION", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=C_ORANGE).pack(anchor="w")
        ctk.CTkLabel(head_box, text="SQUARE SOFT • ESPAÑA (CASTELLANO)", font=ctk.CTkFont(size=10), text_color=C_TEXT_MUTED).pack(anchor="w", pady=(2, 0))

        # Divisor
        div = ctk.CTkFrame(left_panel, height=1, fg_color=C_BORDER)
        div.pack(fill="x", padx=16, pady=(0, 12))

        # Sección de selección de discos
        ctk.CTkLabel(left_panel, text="SELECCIÓN DE DISCO:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(0, 8))

        self.disc_buttons = []
        for d in DISCS_INFO:
            btn = ctk.CTkButton(
                left_panel,
                text=f"💿  {d['title']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                height=38,
                corner_radius=8,
                fg_color=C_ORANGE if self.var_disc.get() == d["id"] else "#151f33",
                hover_color=C_ORANGE_HOVER if self.var_disc.get() == d["id"] else "#1e2c47",
                border_width=1,
                border_color=C_ORANGE if self.var_disc.get() == d["id"] else C_BORDER,
                command=lambda did=d["id"]: self.select_disc(did)
            )
            btn.pack(fill="x", padx=14, pady=4)
            self.disc_buttons.append(btn)

        # Espaciador elástico
        ctk.CTkLabel(left_panel, text="").pack(expand=True)

        # Enlaces de utilidad en el pie izquierdo
        box_links = ctk.CTkFrame(left_panel, fg_color="#0b111c", corner_radius=8, border_width=1, border_color=C_BORDER)
        box_links.pack(fill="x", padx=14, pady=14)

        ctk.CTkButton(box_links, text="📁 Abrir Carpeta de Partidas", font=ctk.CTkFont(size=11), height=28, fg_color="transparent", hover_color="#18253d", anchor="w", command=self.open_saves).pack(fill="x", padx=5, pady=3)
        ctk.CTkButton(box_links, text="💿 Abrir Carpeta de Discos", font=ctk.CTkFont(size=11), height=28, fg_color="transparent", hover_color="#18253d", anchor="w", command=self.open_discs).pack(fill="x", padx=5, pady=3)

        # ── Panel Derecho: Pestañas de configuración estilo Sega Rally / Terranigma ──
        right_panel = ctk.CTkFrame(body, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Pestañas (Tabview)
        self.tabs = ctk.CTkTabview(
            right_panel,
            corner_radius=12,
            fg_color=C_CARD_BG,
            segmented_button_selected_color=C_ORANGE,
            segmented_button_selected_hover_color=C_ORANGE_HOVER,
            segmented_button_unselected_color="#151f33",
            segmented_button_unselected_hover_color="#1e2c47",
            border_width=1,
            border_color=C_BORDER
        )
        self.tabs.pack(fill="both", expand=True)

        tab_play = self.tabs.add("  🚀 INICIO / JUGAR  ")
        tab_enh  = self.tabs.add("  ✨ MEJORAS (QoL)  ")
        tab_gfx  = self.tabs.add("  🖥️ GRÁFICOS  ")
        tab_ctrl = self.tabs.add("  🎮 MANDOS  ")
        tab_sys  = self.tabs.add("  ⚙️ AJUSTES  ")

        self.setup_tab_play(tab_play)
        self.setup_tab_enhancements(tab_enh)
        self.setup_tab_graphics(tab_gfx)
        self.setup_tab_controls(tab_ctrl)
        self.setup_tab_system(tab_sys)

        # ── Barra Inferior Fija de Inicio ──
        footer = ctk.CTkFrame(self, height=70, fg_color=C_CARD_BG, corner_radius=0, border_width=1, border_color=C_BORDER)
        footer.pack(fill="x", side="bottom")

        # Info del mando conectado
        pad_text = detect_gamepad_name()
        self.lbl_pad = ctk.CTkLabel(footer, text=f"🎮 {pad_text}", font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_MUTED)
        self.lbl_pad.pack(side="left", padx=25, pady=16)

        # Botón principal JUGAR AHORA en naranja Sega Rally Revo
        btn_play = ctk.CTkButton(
            footer,
            text="▶ INICIAR JUEGO (4K 60FPS)",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=C_ORANGE,
            hover_color=C_ORANGE_HOVER,
            width=280,
            height=46,
            corner_radius=8,
            command=self.play_game_direct
        )
        btn_play.pack(side="right", padx=25, pady=12)

    def select_disc(self, disc_id):
        self.var_disc.set(disc_id)
        for i, btn in enumerate(self.disc_buttons, 1):
            if i == disc_id:
                btn.configure(fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER, border_color=C_ORANGE)
            else:
                btn.configure(fg_color="#151f33", hover_color="#1e2c47", border_color=C_BORDER)
        self.lbl_disc_desc.configure(text=DISCS_INFO[disc_id - 1]["desc"])

    # ── TAB 1: INICIO Y PRESETS (Estilo Sega Rally / Terranigma) ──
    def setup_tab_play(self, tab):
        # Tarjeta del disco actualmente activo
        disc_box = ctk.CTkFrame(tab, fg_color="#151f33", corner_radius=10, border_width=1, border_color=C_BORDER)
        disc_box.pack(fill="x", padx=16, pady=(14, 10))

        ctk.CTkLabel(disc_box, text="DISCO SELECCIONADO PARA ESTA PARTIDA:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(12, 2))
        self.lbl_disc_desc = ctk.CTkLabel(disc_box, text=DISCS_INFO[self.var_disc.get()-1]["desc"], font=ctk.CTkFont(size=13), text_color=C_TEXT_WHITE, wraplength=620, justify="left")
        self.lbl_disc_desc.pack(anchor="w", padx=16, pady=(0, 12))

        # Tarjetas de Presets Rápidos
        ctk.CTkLabel(tab, text="PERFILES RÁPIDOS DE RENDIMIENTO (PRESETS):", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_TEXT_MUTED).pack(anchor="w", padx=16, pady=(8, 6))

        presets_frame = ctk.CTkFrame(tab, fg_color="transparent")
        presets_frame.pack(fill="x", padx=14, pady=4)

        presets = [
            ("🏎️ MODERNO 4K 60FPS", "Resolución 4K UHD 8x, 16:9 Panorámico, PGXP Subpixel y Cargas Rápidas."),
            ("🎮 ULTRAWIDE 21:9", "Campo de visión panorámico 21:9 adaptado a monitores ultra-anchos."),
            ("📺 RETRO CRT 4:3", "Aspect ratio clásico 4:3 con nitidez pura y Scanlines analógicas."),
        ]

        for title, desc in presets:
            card = ctk.CTkFrame(presets_frame, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
            card.pack(fill="x", pady=4)

            btn = ctk.CTkButton(
                card,
                text=f"Activar: {title}",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=170,
                height=32,
                fg_color="#1e2d4a",
                hover_color=C_ORANGE,
                command=lambda t=title: self.apply_preset(t)
            )
            btn.pack(side="right", padx=14, pady=10)

            t_box = ctk.CTkFrame(card, fg_color="transparent")
            t_box.pack(side="left", fill="both", expand=True, padx=14, pady=8)
            ctk.CTkLabel(t_box, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=C_TEXT_WHITE).pack(anchor="w")
            ctk.CTkLabel(t_box, text=desc, font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED).pack(anchor="w")

        # Resumen de estado
        status_box = ctk.CTkFrame(tab, fg_color="#131c2d", corner_radius=8, border_width=1, border_color=C_BORDER)
        status_box.pack(fill="both", expand=True, padx=16, pady=(10, 14))

        ctk.CTkLabel(status_box, text="ESTADO DEL MOTOR:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=14, pady=(10, 4))
        info_lines = (
            "✓ Recompilación estática nativa C / LLVM Clang 22 (64 bits).\n"
            "✓ Corrección geométrica PGXP activa: cero temblor de polígonos en Squall, escenarios y combates.\n"
            "✓ Soporte de Texturas y Fondos HD activo (mods/texture-packs/SLES-02084).\n"
            "✓ Sin pantallas intermedias: al hacer clic en Iniciar Juego entrará directamente a Final Fantasy VIII."
        )
        ctk.CTkLabel(status_box, text=info_lines, font=ctk.CTkFont(size=12), text_color="#cbd5e1", justify="left").pack(anchor="w", padx=14, pady=(0, 10))

    def apply_preset(self, preset_name):
        if "4K" in preset_name:
            self.var_resolution.set("4K Ultra HD (3840x2160 - 8x SSAA)")
            self.var_aspect.set("16:9 Panorámico")
            self.var_pgxp.set(True)
            self.var_perspective.set(True)
            self.var_turbo_loads.set(True)
            messagebox.showinfo("Perfil Aplicado", "Se ha configurado el perfil Moderno 4K 60FPS Widescreen.")
        elif "ULTRAWIDE" in preset_name:
            self.var_resolution.set("4K Ultra HD (3840x2160 - 8x SSAA)")
            self.var_aspect.set("21:9 Ultra-Panorámico")
            self.var_pgxp.set(True)
            self.var_perspective.set(True)
            messagebox.showinfo("Perfil Aplicado", "Se ha configurado el perfil Ultrawide 21:9.")
        elif "RETRO" in preset_name:
            self.var_resolution.set("1080p Full HD (1920x1080 - 4x)")
            self.var_aspect.set("4:3 Clásico Original")
            messagebox.showinfo("Perfil Aplicado", "Se ha configurado el perfil Retro CRT 4:3.")

    # ── TAB 2: MEJORAS (QoL & Cheats) ──
    def setup_tab_enhancements(self, tab):
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        card1 = ctk.CTkFrame(scroll, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card1.pack(fill="x", pady=6, padx=6)
        ctk.CTkLabel(card1, text="MEJORAS TÉCNICAS Y VISUALES (MOTOR NATIVO)", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_ORANGE).pack(anchor="w", padx=16, pady=(12, 6))

        ctk.CTkCheckBox(card1, text="Precisión Subpixel PGXP (Suprime el temblor poligonal en 3D)", variable=self.var_pgxp, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card1, text="Perspective-Correct Texturing (Texturas de suelos sin deformaciones)", variable=self.var_perspective, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card1, text="Cargas de CD Instantáneas (Cero esperas de lectura de disco)", variable=self.var_turbo_loads, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card1, text="Filtro Bicúbico para FMVs (Suavizado de croma en vídeos CGI)", variable=self.var_bicubic_fmv, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card1, text="Audio SPU de Alta Definición (Interpolación Gaussiana 48 kHz)", variable=self.var_spu_hq, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card1, text="Omitir Cinemáticas FMV (Saltar vídeos pulsando Cancelar/Start)", variable=self.var_skip_fmv, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=(5, 12))

        # Acelerador
        ff_box = ctk.CTkFrame(card1, fg_color="transparent")
        ff_box.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(ff_box, text="⚡ Multiplicador Acelerador Fast-Forward (Tecla Tab / Gatillo R2):", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(ff_box, variable=self.var_ff_speed, values=["2x", "3x", "4x", "8x"], width=85, fg_color="#1e2d4a", button_color=C_ORANGE).pack(side="left")

        # ── Card de Texturas y Fondos HD ──
        card_hd = ctk.CTkFrame(scroll, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card_hd.pack(fill="x", pady=6, padx=6)
        ctk.CTkLabel(card_hd, text="PAQUETES DE TEXTURAS Y FONDOS HD (FORMATO DUCKSTATION / NEXUS)", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_ORANGE).pack(anchor="w", padx=16, pady=(12, 6))

        ctk.CTkCheckBox(card_hd, text="Habilitar Inyección de Texturas y Fondos HD (OpenGL)", variable=self.var_hd_textures, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card_hd, text="Volcar Texturas Originales en Tiempo Real (Texture Dumper / Modo Creador)", variable=self.var_dump_textures, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)

        hd_desc = (
            "Permite sustituir al vuelo las texturas de PS1 por imágenes en 4K/UHD (.png, .jpg, .webp).\n"
            "Compatible con packs de DuckStation y texturas reescaladas con IA (Nexus Mods)."
        )
        ctk.CTkLabel(card_hd, text=hd_desc, font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED, justify="left").pack(anchor="w", padx=16, pady=(2, 6))

        btn_box = ctk.CTkFrame(card_hd, fg_color="transparent")
        btn_box.pack(fill="x", padx=16, pady=(4, 12))
        ctk.CTkButton(btn_box, text="📁 Abrir Carpeta de Texturas HD (replacements)", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1f2d47", hover_color="#2b3e61", border_width=1, border_color=C_BORDER, command=self.open_textures_folder).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_box, text="📁 Abrir Carpeta de Volcados (dumps)", font=ctk.CTkFont(size=12), fg_color="#1f2d47", hover_color="#2b3e61", border_width=1, border_color=C_BORDER, command=self.open_dumps_folder).pack(side="left")

        card2 = ctk.CTkFrame(scroll, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card2.pack(fill="x", pady=6, padx=6)
        ctk.CTkLabel(card2, text="CALIDAD DE VIDA & OPCIONES JUGABLES (OPCIONALES)", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(12, 6))

        ctk.CTkCheckBox(card2, text="Gatillo de Gunblade Automático (Impacto crítico 100% garantizado con Squall)", variable=self.var_gunblade, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card2, text="Desactivar Encuentros Aleatorios (Explora el mapamundi sin interrupciones)", variable=self.var_no_encounters, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card2, text="Finanzas Balamb (Empezar con fondos de Guiles para tiendas)", variable=self.var_max_gil, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)

        ap_box = ctk.CTkFrame(card2, fg_color="transparent")
        ap_box.pack(fill="x", padx=16, pady=(5, 12))
        ctk.CTkLabel(ap_box, text="Multiplicador de PH para Guardian Forces (GFs):", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(ap_box, variable=self.var_ap_boost, values=["Normal (1x)", "2x", "3x", "4x"], width=130, fg_color="#1e2d4a", button_color=C_ORANGE).pack(side="left")

    # ── TAB 3: GRÁFICOS ──
    def setup_tab_graphics(self, tab):
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        card1 = ctk.CTkFrame(scroll, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card1.pack(fill="x", pady=6, padx=6)

        ctk.CTkLabel(card1, text="PANTALLA Y RENDERIZADOR:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_ORANGE).pack(anchor="w", padx=16, pady=(14, 10))

        grid = ctk.CTkFrame(card1, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(grid, text="Resolución Interna:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, sticky="w", pady=8)
        ctk.CTkOptionMenu(grid, variable=self.var_resolution, values=[
            "4K Ultra HD (3840x2160 - 8x SSAA)",
            "1440p Quad HD (2560x1440 - 6x)",
            "1080p Full HD (1920x1080 - 4x)",
            "720p HD (1280x720 - 3x)",
            "240p Original PS1 (1x Pixel Clásico)"
        ], width=290, fg_color="#1e2d4a", button_color=C_ORANGE).grid(row=0, column=1, padx=20, pady=8)

        ctk.CTkLabel(grid, text="Relación de Aspecto:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, sticky="w", pady=8)
        ctk.CTkOptionMenu(grid, variable=self.var_aspect, values=[
            "16:9 Panorámico",
            "21:9 Ultra-Panorámico",
            "4:3 Clásico Original"
        ], width=290, fg_color="#1e2d4a", button_color=C_ORANGE).grid(row=1, column=1, padx=20, pady=8)

        ctk.CTkLabel(grid, text="Sincronización (V-Sync):", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, sticky="w", pady=8)
        ctk.CTkOptionMenu(grid, variable=self.var_vsync, values=[
            "Desactivado (Baja latencia)",
            "Activado (Sin cortes)"
        ], width=290, fg_color="#1e2d4a", button_color=C_ORANGE).grid(row=2, column=1, padx=20, pady=8)

        ctk.CTkCheckBox(card1, text="Pantalla Completa Exclusiva", variable=self.var_fullscreen, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=(12, 14))

        card2 = ctk.CTkFrame(scroll, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card2.pack(fill="x", pady=6, padx=6)

        ctk.CTkLabel(card2, text="TECNOLOGÍAS DE REMASTERIZACIÓN NATIVAS (POST-FX):", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(12, 6))

        ctk.CTkCheckBox(card2, text="Filtro Remaster Cinemático (CAS Sharpening + Filmic Tonemapping + Vibrance)", variable=self.var_remaster_shader, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card2, text="Resplandor Cinemático HDR (Bloom en magias, GFs y chispas sin tocar HUD)", variable=self.var_hdr_bloom, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=5)
        ctk.CTkCheckBox(card2, text="Anti-Aliasing High Quality FXAA (Suavizado de bordes 3D sin perder nitidez)", variable=self.var_fxaa_hq, font=ctk.CTkFont(size=13), checkmark_color=C_ORANGE).pack(anchor="w", padx=16, pady=(5, 12))

    # ── TAB 4: CONTROLES ──
    def setup_tab_controls(self, tab):
        card = ctk.CTkFrame(tab, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        ctk.CTkLabel(card, text="MANDOS Y DISPOSITIVOS:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(14, 10))

        row1 = ctk.CTkFrame(card, fg_color="transparent")
        row1.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(row1, text="Modo de Mando PS1:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=(0, 20))
        ctk.CTkOptionMenu(row1, variable=self.var_pad_mode, values=["DualShock Analógico (Sticks Activos)", "Digital Clásico (Cruceta)"], width=280, fg_color="#1e2d4a", button_color=C_ORANGE).pack(side="left")

        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(row2, text="Zona Muerta Analógica (Deadzone):", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=(0, 20))
        slider = ctk.CTkSlider(row2, from_=0, to=8000, variable=self.var_deadzone, width=200, progress_color=C_ORANGE, button_color=C_ORANGE)
        slider.pack(side="left", padx=(0, 10))
        lbl_val = ctk.CTkLabel(row2, text=f"{int(self.var_deadzone.get() / 327.68)}%", width=45)
        lbl_val.pack(side="left")
        slider.configure(command=lambda v: lbl_val.configure(text=f"{int(float(v) / 327.68)}%"))

        # Controles asignados
        ctk.CTkLabel(card, text="ASIGNACIÓN DE BOTONES (ESTÁNDAR PLAYSTATION / XBOX):", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_TEXT_MUTED).pack(anchor="w", padx=16, pady=(15, 6))

        box_binds = ctk.CTkFrame(card, fg_color="#0b111c", corner_radius=6, border_width=1, border_color=C_BORDER)
        box_binds.pack(fill="x", padx=16, pady=(0, 10))

        t = (
            "• Stick Izquierdo / Cruceta: Mover a Squall y navegar por menús\n"
            "• Botón A / Cruz: Confirmar / Hablar / Examinar\n"
            "• Botón B / Círculo: Cancelar / Salir de menús\n"
            "• Botón X / Cuadrado: Menú principal / Desafiar a Triple Triad (Cartas)\n"
            "• Botón Y / Triángulo: Disparo de Gunblade (Crítico en combate)\n"
            "• L1 + R1: Huir de batalla | Start: Pausa | Select: Mapa"
        )
        ctk.CTkLabel(box_binds, text=t, font=ctk.CTkFont(size=12), text_color="#cbd5e1", justify="left").pack(anchor="w", padx=12, pady=8)

    # ── TAB 5: AJUSTES & SISTEMA ──
    def setup_tab_system(self, tab):
        card = ctk.CTkFrame(tab, fg_color="#151f33", corner_radius=8, border_width=1, border_color=C_BORDER)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        ctk.CTkLabel(card, text="ARCHIVOS DE SISTEMA Y DIAGNÓSTICO:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=16, pady=(14, 10))

        lbl_desc = (
            "Este lanzador configura el juego y lo arranca directamente sin pantallas intermedias.\n"
            "Se ha deshabilitado la generación de archivos basura de diagnóstico psx_freeze_heartbeat.json\n"
            "para garantizar un arranque limpio y el máximo rendimiento."
        )
        ctk.CTkLabel(card, text=lbl_desc, font=ctk.CTkFont(size=12), text_color="#cbd5e1", justify="left").pack(anchor="w", padx=16, pady=(0, 15))

        ctk.CTkButton(card, text="🔄 Restaurar Opciones Recomendadas (4K 60FPS)", fg_color="#1e2d4a", hover_color=C_ORANGE, command=self.restore_defaults).pack(anchor="w", padx=16, pady=6)

    def restore_defaults(self):
        self.var_resolution.set("4K Ultra HD (3840x2160 - 8x SSAA)")
        self.var_aspect.set("16:9 Panorámico")
        self.var_fullscreen.set(False)
        self.var_vsync.set("Desactivado (Baja latencia)")
        self.var_pgxp.set(True)
        self.var_perspective.set(True)
        self.var_turbo_loads.set(True)
        self.var_bicubic_fmv.set(True)
        self.var_spu_hq.set(True)
        self.var_skip_fmv.set(False)
        self.var_pad_mode.set("DualShock Analógico (Sticks Activos)")
        self.var_deadzone.set(3276)
        messagebox.showinfo("Restauración", "Ajustes óptimos recomendados restaurados.")

    def open_saves(self):
        exe, work_dir = find_game_environment()
        s = work_dir / "saves"
        if not s.exists() and (BASE_DIR / "saves").exists(): s = (BASE_DIR / "saves").resolve()
        s.mkdir(parents=True, exist_ok=True)
        os.startfile(str(s))

    def open_discs(self):
        exe, work_dir = find_game_environment()
        d = work_dir / "disc"
        if not d.exists() and (BASE_DIR / "disc").exists(): d = (BASE_DIR / "disc").resolve()
        d.mkdir(parents=True, exist_ok=True)
        os.startfile(str(d))

    def open_textures_folder(self):
        exe, work_dir = find_game_environment()
        t = work_dir / "mods" / "texture-packs" / "SLES-02084" / "replacements"
        if not t.exists() and (BASE_DIR / "mods" / "texture-packs" / "SLES-02084" / "replacements").exists():
            t = (BASE_DIR / "mods" / "texture-packs" / "SLES-02084" / "replacements").resolve()
        t.mkdir(parents=True, exist_ok=True)
        os.startfile(str(t))

    def open_dumps_folder(self):
        exe, work_dir = find_game_environment()
        d = work_dir / "mods" / "texture-packs" / "SLES-02084" / "dumps"
        if not d.exists() and (BASE_DIR / "mods" / "texture-packs" / "SLES-02084" / "dumps").exists():
            d = (BASE_DIR / "mods" / "texture-packs" / "SLES-02084" / "dumps").resolve()
        d.mkdir(parents=True, exist_ok=True)
        os.startfile(str(d))

    def play_game_direct(self):
        """Guarda la configuración y arranca el juego DIRECTO sin segunda ventana"""
        exe, work_dir = find_game_environment()
        if not exe.exists():
            messagebox.showerror("Error", f"No se encontró el ejecutable recompilado:\n{exe}\n\nEn carpeta:\n{work_dir}")
            return

        aspect_val = "16:9"
        if "21:9" in self.var_aspect.get(): aspect_val = "21:9"
        elif "4:3" in self.var_aspect.get(): aspect_val = "4:3"

        disc_id = self.var_disc.get()
        disc_path = DISCS_INFO[disc_id - 1]["cue"]

        settings = {
            "window_width": 3840 if "4K" in self.var_resolution.get() else 1920,
            "fullscreen": self.var_fullscreen.get(),
            "vsync": "off" if "Desactivado" in self.var_vsync.get() else "on",
            "aspect_ratio": aspect_val,
            "fast_forward_speed": int(self.var_ff_speed.get().replace("x", "")),
            "disc_path": disc_path,
            "disc_selected": disc_id,
            "p1_mode": "analog" if "Analógico" in self.var_pad_mode.get() else "digital",
            "deadzone": int(self.var_deadzone.get()),
            "turbo_loads": self.var_turbo_loads.get(),
            "auto_skip_fmv": self.var_skip_fmv.get(),
            "pgxp_geometry": self.var_pgxp.get(),
            "pgxp_perspective": self.var_perspective.get(),
            "bicubic_fmv": self.var_bicubic_fmv.get(),
            "spu_hq": self.var_spu_hq.get(),
            "gunblade_perfect": self.var_gunblade.get(),
            "no_encounters": self.var_no_encounters.get(),
            "ap_boost": 1 if "Normal" in self.var_ap_boost.get() else int(self.var_ap_boost.get().replace("x", "")),
            "max_gil": self.var_max_gil.get(),
            "hd_textures": self.var_hd_textures.get(),
            "dump_textures": self.var_dump_textures.get(),
            "remaster_shader": self.var_remaster_shader.get(),
            "hdr_bloom": self.var_hdr_bloom.get(),
            "fxaa_hq": self.var_fxaa_hq.get(),
        }
        save_game_settings(settings)

        # Variables de entorno para omitir Dear ImGui y arrancar juego directamente
        env = os.environ.copy()
        env["PSX_NO_LAUNCHER"] = "1"
        env["PSX_RENDER_THREAD"] = "0"
        env["PSX_PRESENT_THREAD"] = "0"
        env["PSX_FRAME_GEN"] = "0"
        env["PSX_FRAME_INTERPOLATION"] = "0"
        env["PSX_VSYNC"] = "0" if "Desactivado" in self.var_vsync.get() else "1"
        env["PSX_FPS_TELEMETRY"] = "0"
        env["PSX_FREEZE_HEARTBEAT"] = "0"

        if self.var_remaster_shader.get():
            env["PSX_POST_SHADER"] = "shaders/remaster_cinematic.pfx"
        else:
            env["PSX_POST_SHADER"] = ""

        if self.var_hdr_bloom.get():
            env["PSX_BLOOM"] = "0.40"
        else:
            env["PSX_BLOOM"] = "0.0"

        if self.var_fxaa_hq.get():
            env["PSX_AA_MODE"] = "fxaa_hq"
        else:
            env["PSX_AA_MODE"] = "off"

        env["PSX_SUPERSAMPLE"] = "2.0"

        if "21:9" in self.var_aspect.get():
            env["PSX_ASPECT_RATIO"] = "21:9"
            env["PSX_WS_FORCE_3D"] = "1"
            env["PSX_WS_FORCE_2D"] = "0"
        elif "4:3" in self.var_aspect.get():
            env["PSX_ASPECT_RATIO"] = "4:3"
            env["PSX_WS_FORCE_3D"] = "0"
            env["PSX_WS_FORCE_2D"] = "1"
        else:
            env["PSX_ASPECT_RATIO"] = "16:9"
            env["PSX_WS_FORCE_3D"] = "1"
            env["PSX_WS_FORCE_2D"] = "0"

        if "4K" in self.var_resolution.get(): env["PSX_INTERNAL_SCALE"] = "8"
        elif "1440p" in self.var_resolution.get(): env["PSX_INTERNAL_SCALE"] = "6"
        elif "1080p" in self.var_resolution.get(): env["PSX_INTERNAL_SCALE"] = "4"
        elif "720p" in self.var_resolution.get(): env["PSX_INTERNAL_SCALE"] = "3"
        else: env["PSX_INTERNAL_SCALE"] = "1"

        # Comando directo con --no-launcher (NUNCA abre la segunda ventana Dear ImGui)
        cmd = [str(exe), "--no-launcher"]

        # Lanzar proceso independiente en la carpeta del juego
        subprocess.Popen(cmd, cwd=str(work_dir), env=env)

        # Cerrar el lanzador
        self.destroy()

def main():
    app = FF8ModernLauncher()
    app.mainloop()

if __name__ == "__main__":
    main()
