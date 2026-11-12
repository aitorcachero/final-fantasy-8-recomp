<div align="center">

# ⚔️ Final Fantasy VIII Recompiled (PC Port Nativo x64 — Master Edition)

### *Port nativo para PC (Windows x64) mediante ingeniería inversa y recompilación estática LLVM*

[![Platform](https://img.shields.io/badge/Plataforma-Windows%20x64%20Nativo-blue.svg?style=for-the-badge&logo=windows)](https://github.com/aitorcachero/final-fantasy-8-recomp)
[![Resolution](https://img.shields.io/badge/Resoluci%C3%B3n-Nativa%204K%20UHD%20(3840x2160)-brightgreen.svg?style=for-the-badge)](https://github.com/aitorcachero/final-fantasy-8-recomp)
[![Framerate](https://img.shields.io/badge/Refresco-60%20FPS%20%2F%20VBlank%20Pacing-orange.svg?style=for-the-badge)](https://github.com/aitorcachero/final-fantasy-8-recomp)
[![Aspect Ratio](https://img.shields.io/badge/Aspecto-16%3A9%20%2F%2021%3A9%20Ultrawide-purple.svg?style=for-the-badge)](https://github.com/aitorcachero/final-fantasy-8-recomp)
[![PGXP](https://img.shields.io/badge/Geometr%C3%ADa-PGXP%20Subpixel%20Precision-red.svg?style=for-the-badge)](https://github.com/aitorcachero/final-fantasy-8-recomp)
[![License](https://img.shields.io/badge/Licencia-MIT-green.svg?style=for-the-badge)](LICENSE)

---

</div>

## 📖 Descripción

**Final Fantasy VIII Recompiled** es un port nativo para PC (Windows x64) del legendario JRPG de 1999 desarrollado por **Square Soft** para la consola PlayStation 1.

A diferencia de los emuladores tradicionales que interpretan en tiempo real la CPU MIPS R3000A, este proyecto emplea recompilación estática anticipada (AOT) mediante **psxrecomp** y el ecosistema LLVM/Clang. Todo el código máquina del juego se traduce a C nativo optimizado y se enlaza directamente contra un backend gráfico moderno OpenGL de alto rendimiento.

El resultado es una aplicación nativa de 64 bits con latencia prácticamente nula, consumo mínimo de recursos, compatibilidad completa para los 4 CDs con cambio dinámico de disco, y una fidelidad gráfica y de audio superior a la versión de consola original.

---

## ✨ Características Principales

* 🖥️ **Resolución Interna 4K Ultra HD:** Escalado de renderizado de alta precisión con supersampling SSAA 2.0x, filtrado bilineal y filtrado anisotrópico 16x.
* 📐 **Relación de Aspecto Panorámica 16:9 y 21:9 Ultrawide:** Campo de visión ampliado nativamente para monitores modernos sin bandas negras ni estiramiento de geometrías.
* 💎 **PGXP Subpixel Precision:** Supresión total del temblor poligonal (*polygon jitter/wobble*) típico de PS1 en personajes, mapamundi 3D y secuencias de combate.
* 🔍 **Perspective-Correct Texturing:** Corrección de la distorsión de texturas afines en polígonos 3D para un aspecto nítido y estable en todos los ángulos de cámara.
* 🎬 **Cinemáticas CGI Mejoradas (FMV):** Filtrado bicúbico con suavizado de croma para una reproducción limpia de las secuencias de vídeo pre-renderizadas.
* 🎼 **Audio SPU HQ:** Motor de sonido PlayStation de 24 canales con interpolación Gaussiana de alta fidelidad, remuestreo a 48 kHz y búfer de latencia ultrabaja.
* 💿 **Soporte Completo de 4 CDs:** Gestión integrada de los 4 discos del juego. Selección y cambio de disco dinámico desde el lanzador y en caliente.
* 🕹️ **Control Analógico DualShock:** Compatibilidad total para sticks analógicos, vibración y detección directa de mandos modernos (Xbox, PlayStation DualSense/DualShock, DirectInput/XInput).
* 🌟 **Pipeline de Remasterización Nativo (Post-Processing GLSL):**
  * **Contrast Adaptive Sharpening (CAS):** Enfoque adaptativo inteligente que resalta el detalle fino de los fondos prerrenderizados (Jardín de Balamb, Timber, Deling City) sin generar halos ni ruido.
  * **Resplandor Cinemático HDR (Bloom Selectivo):** Resplandor lumínico de alta precisión en magias, invocaciones de Guardian Forces (GFs), chispas de Gunblade y efectos visuales con máscara stencil (las cajas de texto y el HUD permanecen 100% nítidos).
  * **Anti-Aliasing High Quality FXAA:** Suavizado subpíxel de bordes poligonales sin pérdida de definición de textura.
  * **Filmic Tonemapping & Vibrance:** Curva de contraste cinematográfica y realce de color perceptual que revitaliza la paleta visual original de 1999.
* 🛡️ **Bypass Nativo de Protección LibCrypt:** Rutina de intercepción automática en RAM para evitar cualquier bloqueo o pantallazo negro por comprobación anti-copia de sectores.
* 🖼️ **Inyección y Reemplazo de Texturas HD:** Compatibilidad nativa en el pipeline OpenGL con el estándar de DuckStation y Beetle PSX. Permite sustituir al vuelo texturas de PS1 por imágenes en 4K/UHD (`.png`, `.webp`, `.jpg`) con filtrado de transparencias y escalado bilineal.
* 🎨 **Volcado de Texturas en Tiempo Real (Texture Dumper):** Modo creador integrado que extrae de forma limpia las texturas originales de la VRAM mientras juegas para poder editarlas o reescalarlas con IA (ESRGAN).
* 🚀 **Lanzador Único Moderno (Estilo Sega Rally Revo / Terranigma):** Interfaz oscura neumórfica para elegir disco, ajustar resoluciones, gestionar texturas HD, ver estado del mando e iniciar el juego en un solo clic.

---

## 🖼️ Paquetes de Texturas HD y Modding Visual

Este port nativo incluye un subsistema de texturas HD de alto rendimiento integrado directamente en el backend de renderizado OpenGL, **100% compatible con la nomenclatura y estructura de paquetes de DuckStation**:

### ⚡ Instalación Automatizada en 1-Clic:
Dispones del script `INSTALAR_PACK_TEXTURAS_HD.bat` en la raíz del juego:
1. **Arrastra y suelta** cualquier archivo comprimido (`.zip`, `.rar`, `.7z`) o carpeta que contenga un pack de texturas sobre `INSTALAR_PACK_TEXTURAS_HD.bat`.
2. El instalador extraerá las imágenes, las organizará en la ruta canónica de la versión española (`mods/texture-packs/SLES-02084/replacements/`) y activará automáticamente el mod en `mods/state.toml`.

### 📂 Estructura de Directorios de Texturas:
* `mods/texture-packs/SLES-02084/replacements/`: Carpeta donde se alojan las texturas HD de reemplazo (`texupload-*.png`, `texpage-*.png`, etc.).
* `mods/texture-packs/SLES-02084/dumps/`: Carpeta donde el motor guarda las texturas extraídas de la VRAM al activar el modo *Texture Dumper*.
* `mods/texture-packs/SLES-02084/config.yaml`: Parámetros de precisión y caché optimizados específicamente para *Final Fantasy VIII*:
  * `MaxVRAMWriteSplits: 4` (tratamiento de escrituras parciales de VRAM).
  * `ConvertCopiesToWrites: true` (manejo correcto de copias de VRAM en animaciones).
  * `ReplacementScaleLinearFilter: true` (suavizado bilineal en texturas de alta resolución).

### 🎛️ Control desde el Master Launcher:
Dentro de la pestaña **MEJORAS (QoL)** del lanzador dispones de:
* Casilla para **activar/desactivar el reemplazo de texturas HD** con un clic.
* Casilla para **activar el volcado de texturas (Texture Dumper)** en tiempo real.
* Botón **"📁 Abrir Carpeta de Texturas HD (replacements)"** para acceder al instante mediante el Explorador de Windows.
* Botón **"📁 Abrir Carpeta de Volcados (dumps)"** para revisar las texturas capturadas.

---

## 🚀 Guía de Instalación Rápida (Para Jugadores)

> **Nota de preservación legal:** Este repositorio **NO** incluye ni distribuye las imágenes comerciales protegidas de Final Fantasy VIII. Debes suministrar tus propias copias de los 4 CDs originales.

1. Descarga el paquete compilado desde la sección **[Releases](https://github.com/aitorcachero/final-fantasy-8-recomp/releases)**:
   - `Final_Fantasy_VIII_Recompiled_v1.0_Windows_x64.zip`
2. Descomprime el archivo en la carpeta que prefieras.
3. Copia tus imágenes de disco de Final Fantasy VIII (en formato `.bin/.cue` o `.chd`) en la carpeta `disc/`:
   - `disc/Final Fantasy VIII (Spain) (Disc 1).cue` (y sus `.bin` correspondientes para Discos 1 a 4).
4. Ejecuta `Final_Fantasy_VIII_Launcher.exe`.
5. Selecciona el disco activo (Disco 1 para partida nueva), configura tu resolución preferida y haz clic en **INICIAR JUEGO (4K 60FPS)**.

---

## 🛠️ Compilación desde el Código Fuente

### Requisitos:
* **Compilador C/C++:** Clang 18+ o GCC 13+ (compatible con C11 / C++20).
* **Sistema de compilación:** CMake 3.25+ y Ninja.
* **SDK:** Windows 10/11 SDK.

### Pasos de compilación:
```bash
git clone --recursive https://github.com/aitorcachero/final-fantasy-8-recomp.git
cd final-fantasy-8-recomp

# Configurar con CMake
cmake -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release

# Compilar el ejecutable principal
ninja -C build-release Final_Fantasy_VIII_Recompiled.exe
```

---

## ⚖️ Licencia y Créditos

* **Desarrollo del juego original:** Square Soft (Square Enix), 1999.
* **Recompilación estática:** Basado en el framework [psxrecomp](https://github.com/RetroPortingToolKit/psxrecomp).
* **Licencia del proyecto:** MIT License. Consulte el archivo `LICENSE` para más detalles.
