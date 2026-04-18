import os
os.makedirs("/home/user/output/mp3-downloader", exist_ok=True)

# app.py - servidor Flask
app_py = '''# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import threading

app = Flask(__name__)

FFMPEG_PATH = r"C:\\Users\\droid\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.1-full_build\\bin"
DOWNLOAD_FOLDER = "./downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

descarga_estado = {"progreso": 0, "estado": "idle", "archivo": "", "error": ""}

def hook_progreso(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        descargado = d.get("downloaded_bytes", 0)
        if total:
            descarga_estado["progreso"] = int(descargado / total * 100)
            descarga_estado["estado"] = "descargando"
    elif d["status"] == "finished":
        descarga_estado["estado"] = "convirtiendo"

def descargar(url, calidad):
    descarga_estado.update({"progreso": 0, "estado": "iniciando", "archivo": "", "error": ""})
    opciones = {
        "format": "bestaudio/best",
        "ffmpeg_location": FFMPEG_PATH,
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [hook_progreso],
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": calidad},
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "writethumbnail": True,
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get("title", "audio")
            archivo_mp3 = os.path.join(DOWNLOAD_FOLDER, f"{titulo}.mp3")
            descarga_estado.update({"estado": "listo", "progreso": 100, "archivo": archivo_mp3})
    except Exception as e:
        descarga_estado.update({"estado": "error", "error": str(e)})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/descargar", methods=["POST"])
def iniciar_descarga():
    data = request.get_json()
    url = data.get("url", "").strip()
    calidad = data.get("calidad", "320")
    if not url:
        return jsonify({"error": "URL vacia"}), 400
    hilo = threading.Thread(target=descargar, args=(url, calidad))
    hilo.start()
    return jsonify({"ok": True})

@app.route("/estado")
def estado():
    return jsonify(descarga_estado)

@app.route("/obtener")
def obtener_archivo():
    archivo = descarga_estado.get("archivo", "")
    if archivo and os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    return jsonify({"error": "Archivo no disponible"}), 404

if __name__ == "__main__":
    print("Servidor corriendo en http://localhost:5000")
    app.run(debug=False, host="0.0.0.0", port=5000)
'''

# templates/index.html
index_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MP3 Downloader</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f0f0f;
            color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 520px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        h1 {
            font-size: 1.6rem;
            margin-bottom: 8px;
            color: #fff;
        }
        p.sub {
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 28px;
        }
        label {
            font-size: 0.85rem;
            color: #aaa;
            display: block;
            margin-bottom: 6px;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            background: #111;
            border: 1px solid #333;
            border-radius: 10px;
            color: #fff;
            font-size: 0.95rem;
            margin-bottom: 16px;
            outline: none;
            transition: border 0.2s;
        }
        input[type="text"]:focus { border-color: #1db954; }
        select {
            width: 100%;
            padding: 12px 16px;
            background: #111;
            border: 1px solid #333;
            border-radius: 10px;
            color: #fff;
            font-size: 0.95rem;
            margin-bottom: 24px;
            outline: none;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #1db954;
            color: #000;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #17a349; }
        button:disabled { background: #444; color: #888; cursor: not-allowed; }
        .progreso-wrap {
            margin-top: 24px;
            display: none;
        }
        .barra-bg {
            background: #2a2a2a;
            border-radius: 999px;
            height: 8px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .barra {
            height: 100%;
            background: #1db954;
            width: 0%;
            transition: width 0.3s;
            border-radius: 999px;
        }
        .estado-texto {
            font-size: 0.85rem;
            color: #aaa;
            text-align: center;
        }
        .btn-dl {
            margin-top: 16px;
            background: #2a2a2a;
            color: #1db954;
            display: none;
        }
        .btn-dl:hover { background: #333; }
        .error { color: #ff5555; font-size: 0.85rem; margin-top: 12px; text-align: center; }
    </style>
</head>
<body>
<div class="card">
    <h1>MP3 Downloader</h1>
    <p class="sub">Pega la URL de YouTube y descarga el audio en MP3</p>

    <label>URL del video</label>
    <input type="text" id="url" placeholder="https://www.youtube.com/watch?v=...">

    <label>Calidad</label>
    <select id="calidad">
        <option value="320">320 kbps (maxima)</option>
        <option value="256">256 kbps</option>
        <option value="192">192 kbps</option>
        <option value="128">128 kbps</option>
        <option value="0">Auto</option>
    </select>

    <button id="btnDescargar" onclick="iniciarDescarga()">Descargar MP3</button>

    <div class="progreso-wrap" id="progresoWrap">
        <div class="barra-bg"><div class="barra" id="barra"></div></div>
        <div class="estado-texto" id="estadoTexto">Iniciando...</div>
        <div class="error" id="errorTexto"></div>
        <button class="btn-dl" id="btnObtener" onclick="obtenerArchivo()">Guardar MP3</button>
    </div>
</div>

<script>
let intervalo = null;

function iniciarDescarga() {
    const url = document.getElementById("url").value.trim();
    const calidad = document.getElementById("calidad").value;
    if (!url) return alert("Ingresa una URL");

    document.getElementById("btnDescargar").disabled = true;
    document.getElementById("progresoWrap").style.display = "block";
    document.getElementById("btnObtener").style.display = "none";
    document.getElementById("errorTexto").textContent = "";
    document.getElementById("barra").style.width = "0%";
    document.getElementById("estadoTexto").textContent = "Iniciando...";

    fetch("/descargar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, calidad })
    }).then(() => {
        intervalo = setInterval(verificarEstado, 800);
    });
}

function verificarEstado() {
    fetch("/estado").then(r => r.json()).then(data => {
        const textos = {
            "idle": "Esperando...",
            "iniciando": "Iniciando descarga...",
            "descargando": `Descargando... ${data.progreso}%`,
            "convirtiendo": "Convirtiendo a MP3...",
            "listo": "Listo!",
            "error": "Error"
        };
        document.getElementById("estadoTexto").textContent = textos[data.estado] || data.estado;
        document.getElementById("barra").style.width = data.progreso + "%";

        if (data.estado === "listo") {
            clearInterval(intervalo);
            document.getElementById("btnObtener").style.display = "block";
            document.getElementById("btnDescargar").disabled = false;
        } else if (data.estado === "error") {
            clearInterval(intervalo);
            document.getElementById("errorTexto").textContent = data.error;
            document.getElementById("btnDescargar").disabled = false;
        }
    });
}

function obtenerArchivo() {
    window.location.href = "/obtener";
}
</script>
</body>
</html>
'''

os.makedirs("/home/user/output/mp3-downloader/templates", exist_ok=True)

with open("/home/user/output/mp3-downloader/app.py", "w", encoding="utf-8") as f:
    f.write(app_py)

with open("/home/user/output/mp3-downloader/templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

# Actualizar requirements.txt
with open("/home/user/output/mp3-downloader/requirements.txt", "w") as f:
    f.write("yt-dlp>=2024.1.0\nflask>=3.0.0\n")

print("Archivos generados:")
for root, dirs, files in os.walk("/home/user/output/mp3-downloader"):
    for file in files:
        print(f"  {os.path.join(root, file).replace('/home/user/output/mp3-downloader/', '')}")