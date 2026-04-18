# 🎵 TuneGrab — by MatiDroid

Descarga canciones de YouTube directamente como MP3, sin anuncios, sin webs maliciosas, desde tu propio computador.

---

## ¿Qué necesitas antes de empezar?

Antes de usar esta aplicación, necesitas instalar 3 cosas en tu computador. No te preocupes, es simple y solo se hace **una vez**.

---

### Paso 1 — Instalar Python

Python es el lenguaje en el que está hecho este programa.

1. Ve a 👉 https://www.python.org/downloads/
2. Haz clic en el botón amarillo grande que dice **"Download Python"**
3. Abre el instalador descargado
4. **MUY IMPORTANTE:** Antes de hacer clic en "Install Now", marca la casilla ✅ **"Add Python to PATH"**
5. Haz clic en **"Install Now"** y espera que termine

Para verificar, abre PowerShell y escribe:
```
python --version
```
Si ves `Python 3.x.x`, está listo ✅

---

### Paso 2 — Instalar ffmpeg

ffmpeg es el programa que convierte el audio al formato MP3.

1. Abre PowerShell como **Administrador** (clic derecho → "Ejecutar como administrador")
2. Escribe y presiona Enter:
```
winget install ffmpeg
```
3. Cuando diga **"Instalado correctamente"**, cierra y vuelve a abrir PowerShell

Verifica:
```
ffmpeg -version
```
Si ves información de ffmpeg, está listo ✅

> ⚠️ Si `ffmpeg -version` no responde, cierra PowerShell completamente y vuelve a abrirlo como Administrador antes de continuar.

---

### Paso 3 — Descargar este proyecto

**Opción A — Sin Git (más simple):**
1. En esta página de GitHub, haz clic en el botón verde **"Code"**
2. Selecciona **"Download ZIP"**
3. Descomprime el ZIP en tu Escritorio

**Opción B — Con Git:**
```
git clone https://github.com/MatiDroid21/TuneGrab.git
```

---

### Paso 4 — Instalar las dependencias

1. Abre PowerShell y navega a la carpeta del proyecto:
```
cd C:\Users\TU_NOMBRE\Desktop\TuneGrab
```
> 💡 Reemplaza `TU_NOMBRE` con tu nombre de usuario de Windows

2. Ejecuta:
```
pip install -r requirements.txt
```
Esto instala automáticamente **yt-dlp** y **Flask** (todo lo necesario). Solo se hace una vez ✅

---

## ¿Cómo usar la aplicación?

### 🌐 Opción A — Interfaz web (la más fácil)

1. Abre PowerShell en la carpeta del proyecto y ejecuta:
```
python app.py
```
2. Abre tu navegador (Chrome, Edge, Firefox) y ve a:
```
http://localhost:5000
```
3. Pega la URL de YouTube, elige la calidad y haz clic en **"Descargar MP3"**
4. Cuando aparezca el botón **"Guardar MP3"**, haz clic para guardarlo en tu computador

> Para cerrar el servidor, vuelve a PowerShell y presiona `Ctrl + C`

---

### 💻 Opción B — Desde la terminal

```
python downloader.py "URL_DEL_VIDEO" -q 320
```

**Ejemplos:**
```
# Maxima calidad
python downloader.py "https://www.youtube.com/watch?v=XXXXXXX"

# Calidad especifica
python downloader.py "https://www.youtube.com/watch?v=XXXXXXX" -q 192

# Carpeta personalizada
python downloader.py "https://www.youtube.com/watch?v=XXXXXXX" -o "C:/Musica"
```
> ⚠️ Siempre pon la URL entre comillas dobles `" "`. Si la URL tiene el símbolo `&`, es obligatorio.

Los archivos se guardan en la carpeta `downloads/` dentro del proyecto.

---

## Preguntas frecuentes

**¿De dónde saco la URL?**
En YouTube, clic derecho sobre el video → "Copiar URL del video". O copia lo que aparece en la barra de direcciones del navegador.

**¿Qué calidad elijo?**
- **320 kbps** → Máxima calidad (recomendado)
- **192 kbps** → Buena calidad, archivo más liviano
- **128 kbps** → Calidad básica, archivo pequeño

**¿Solo funciona con YouTube?**
No, también funciona con SoundCloud, Vimeo, TikTok y miles de sitios más.

**Error: "yt-dlp no está instalado"**
Ejecuta: `pip install yt-dlp`

**Error: "ffmpeg not found"**
Revisa el Paso 2 de esta guía. Asegúrate de haber instalado ffmpeg como Administrador y de haber cerrado y reabierto PowerShell después.

**Error: "No module named flask"**
Ejecuta: `pip install flask`

---

## Estructura del proyecto

```
TuneGrab/
├── app.py              → Servidor web (interfaz gráfica)
├── downloader.py       → Script de terminal
├── templates/
│   └── index.html      → Página web de la interfaz
├── requirements.txt    → Lista de dependencias
└── downloads/          → Aquí se guardan los MP3 (se crea automáticamente)
```

---

## Licencia

MIT — Puedes usar, modificar y compartir este proyecto libremente.  
Creado por **MatiDroid** 🎧

Sean Felices :D
