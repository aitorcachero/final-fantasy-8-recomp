[size=150][b][PS1 Recomp] Final Fantasy VIII (Español / PAL) - Port Nativo para PC v1.0 (4K UHD SSAA 2.0x, PGXP Subpixel sin Wobble, 16:9/21:9 Ultrawide, Soporte 4 CDs, Audio SPU HQ 48kHz, Master Launcher Moderno)[/b][/size]

¡Muy buenas a toda la comunidad de [b]ElOtroLado[/b]!

Tras mucho trabajo de optimización y depuración de rutinas de ejecución, por fin os traigo la **v1.0 definitiva** del port nativo para PC (Windows x64) de una de las obras cumbre de Square y del catálogo de PlayStation 1 completamente en castellano: [b]Final Fantasy VIII[/b] (Edición PAL España, [i]SLES-02084[/i]), impulsado por ingeniería inversa y recompilación estática anticipada (AOT) con el framework [i]psxrecomp[/i] y el ecosistema LLVM/Clang.

Al igual que en los proyectos que hemos compartido anteriormente, [b]NO SE TRATA DE UN EMULADOR[/b]. No hay capas de traducción en tiempo real ni sobrecarga de emulación: las instrucciones de la CPU MIPS R3000A han sido recompiladas de antemano a código C nativo y enlazadas directamente a las APIs gráficas modernas de 64 bits. El resultado es latencia prácticamente cero, framerate estable a 60 FPS con sincronización VBlank perfecta, consumo mínimo de hardware y una fidelidad gráfica y de sonido que lleva a Squall, Rinoa y el jardín de Balamb a un estándar visual contemporáneo.

---

[b][size=120]🚀 Novedades y Mejoras Clave de esta Master Edition:[/size][/b]

[list]
[*] [b]Master Launcher Moderno estilo Sega Rally Revo / Terranigma Recomp:[/b]
  Se acabaron las múltiples ventanas intermedias o consolas de depuración. Todo el juego se controla desde una interfaz oscura neumórfica integrada ([i]Deep Slate Navy & Vibrant Orange[/i]) que permite seleccionar el disco activo (CD 1 a 4), consultar y ajustar todas las mejoras gráficas y de audio, ver el estado de los mandos conectados e iniciar el juego en un solo clic.

[*] [b]Resolución Interna 4K Ultra HD (3840x2160) con SSAA 2.0x:[/b]
  Renderizado de geometría de alta precisión que elimina el clásico aspecto pixelado y borroso de los polígonos originales de 32 bits, acompañado de filtrado anisotrópico 16x y filtrado de texturas con corrección de perspectiva.

[*] [b]Geometría PGXP Subpixel Precision (Supresión total del temblor poligonal):[/b]
  Corrige el mayor defecto visual de la primera PlayStation: la falta de subpíxeles y el temblor constante de vértices (*polygon wobble / jitter*). Los modelos de Squall, Seifer, los enemigos, los GF (Guardian Forces) y el mapamundi 3D lucen sólidos y estables como si fuesen de consolas de generaciones posteriores.

[*] [b]Perspective-Correct Texturing:[/b]
  Elimina la deformación trapezoidal afín de las texturas de PlayStation al rotar la cámara en el mapamundi o en los escenarios de combate.

[*] [b]Aspect Ratio Panorámico 16:9 y 21:9 Ultrawide Nativo:[/b]
  Ampliación real del campo de visión (FOV) sin bandas negras forzadas ni estiramiento de geometrías. También se incluye el modo clásico 4:3 con bordes limpios para los puristas que deseen la experiencia de tubo CRT original.

[*] [b]Cinemáticas CGI Mejoradas (FMV):[/b]
  Reproducción de las míticas secuencias pre-renderizadas (la batalla inicial Squall vs Seifer, el baile de graduación, el desembarco en Dollet...) con escalado bicúbico y filtrado de croma para suavizar los bloques de compresión del códec MDEC original.

[*] [b]Audio SPU HQ a 48 kHz (Interpolación Gaussiana):[/b]
  Motor de audio PlayStation de 24 canales con interpolación Gaussiana de alta fidelidad, remuestreo a 48.000 Hz estéreo y búfer de latencia ultrabaja. La legendaria banda sonora de Nobuo Uematsu (*Liberi Fatali*, *Eyes on Me*, *The Man with the Machine Gun*) suena con una claridad asombrosa.

[*] [b]Soporte Completo de los 4 CDs con Cambio Dinámico:[/b]
  Gestión transparente de los 4 discos del juego. Puedes seleccionar el disco desde el propio launcher o cambiar de CD en caliente cuando el juego lo requiera al avanzar en la historia.

[*] [b]Bypass Automático Anti-Copia LibCrypt PAL:[/b]
  La versión europea/española de Final Fantasy VIII incluye protección LibCrypt con verificación de sectores subcanal. Se ha implementado un bypass a nivel de instrucción que detecta los bucles de comprobación en RAM y salta limpiamente a la inicialización del juego, evitando cualquier bloqueo o pantallazo negro.

[*] [b]Soporte Nativo de Texturas y Fondos HD (Interoperabilidad DuckStation & Beetle):[/b]
  Integración directa en el pipeline OpenGL para reemplazar texturas clásicas de PS1 por imágenes en 4K/UHD ([i].png, .webp, .jpg[/i]). Cuenta además con [b]Texture Dumper[/b] en tiempo real para creadores de mods y un script [b]INSTALAR_PACK_TEXTURAS_HD.bat[/b] que permite arrastrar y soltar cualquier .zip/.rar de texturas para instalarlo automáticamente.

[*] [b]Control Analógico DualShock Plug & Play:[/b]
  Soporte completo y precalibrado para mandos de Xbox (Series / One / 360), PlayStation (DualShock 4 / DualSense), Nintendo Switch Pro y gamepads USB DirectInput/XInput, con los sticks analógicos habilitados por defecto.
[/list]

---

[b][size=120]📦 Enlaces de Descarga y Repositorio Oficial:[/size][/b]

[list]
[*] [b]Repositorio en GitHub (Código fuente completo y documentación):[/b]
  [url=https://github.com/aitorcachero/final-fantasy-8-recomp]https://github.com/aitorcachero/final-fantasy-8-recomp[/url]

[*] [b]Página de Releases (Descarga v1.0.0 Windows x64):[/b]
  [url=https://github.com/aitorcachero/final-fantasy-8-recomp/releases/tag/v1.0.0]https://github.com/aitorcachero/final-fantasy-8-recomp/releases/tag/v1.0.0[/url]

[*] [b]Enlace de descarga directa del paquete ZIP (39.89 MB):[/b]
  [url=https://github.com/aitorcachero/final-fantasy-8-recomp/releases/download/v1.0.0/Final_Fantasy_VIII_Recompiled_v1.0_Windows_x64.zip]Final_Fantasy_VIII_Recompiled_v1.0_Windows_x64.zip[/url]
[/list]

---

[b][size=120]🎮 ¿Cómo se juega? (Guía Rápida en 4 Pasos):[/size][/b]

[quote]
[b]Nota de preservación legal:[/b] Por razones legales y de propiedad intelectual, el paquete de distribución [b]NO[/b] incluye las imágenes de disco comerciales de Square Soft. Debes disponer de tus propias copias de los 4 CDs originales.
[/quote]

1. [b]Descargar y descomprimir:[/b] Descarga [i]Final_Fantasy_VIII_Recompiled_v1.0_Windows_x64.zip[/i] y extráelo en cualquier carpeta de tu disco duro.
2. [b]Copiar los discos:[/b] Copia tus 4 imágenes de disco de Final Fantasy VIII (en formato [i].bin/.cue[/i], [i].chd[/i], o [i].iso[/i]) dentro de la subcarpeta [b]disc/[/b] (o directamente en la raíz de la carpeta del juego).
   [i]* Consejo: Si tienes archivos .cue/.bin estándar, el launcher los detectará y enlazará automáticamente sin necesidad de conversiones.*[/i]
3. [b]Abrir el Master Launcher:[/b] Haz doble clic en [b]Final_Fantasy_VIII_Launcher.exe[/b] (o en [i]CONFIGURAR_FINAL_FANTASY_VIII.bat[/i]).
4. [b]¡A jugar!:[/b] Asegúrate de que el [b]CD 1[/b] está seleccionado (si vas a comenzar nueva partida), comprueba que tu mando aparezca como detectado y pulsa el botón grande [b]INICIAR JUEGO (4K 60FPS)[/b].

---

[b][size=120]⌨️ Controles por Defecto:[/size][/b]

[list]
[*] [b]Mandos (Xbox / PlayStation / Switch Pro / DirectInput):[/b]
  * Stick izquierdo / D-Pad: Movimiento en 8 direcciones
  * Botón A / Cruz: Aceptar / Hablar / Examinar
  * Botón B / Círculo: Cancelar / Menú rápido
  * Botón X / Cuadrado: Desafiar a cartas (Triple Triad) / Menú de opciones
  * Botón Y / Triángulo: Abrir Menú Principal (Enlaces, GF, Magias)
  * L1 / R1: Cambiar objetivo / Huir de combate (L2+R2)
  * Start / Options: Pausa
  * Select / Share: Alternar mapa en el mapamundi
[*] [b]Teclado:[/b]
  * Flechas de dirección: Mover a Squall
  * X: Aceptar
  * C: Cancelar
  * V: Menú de Cartas / Opciones
  * Z: Menú Principal
  * Q / E: L1 / R1
  * Enter: Start
  * Espacio: Select
[/list]

---

¡Espero que lo disfrutéis tanto como yo haciéndolo! Cualquier duda, problema de configuración o sugerencia podéis comentarla directamente en este hilo y la vamos revisando. ¡A salvar el mundo de Artemisa en glorioso 4K!
