# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import shutil
import threading

app = Flask(__name__)

DOWNLOAD_FOLDER = "./downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_ffmpeg_path():
    ruta = shutil.which("ffmpeg")
    if ruta:
        return os.path.dirname(ruta)
    return None

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

    ffmpeg = get_ffmpeg_path()
    if ffmpeg:
        opciones["ffmpeg_location"] = ffmpeg

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
