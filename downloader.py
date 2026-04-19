# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import yt_dlp

COOKIE_FILE = "cookies.txt"

def get_ffmpeg_path():
    ruta = shutil.which("ffmpeg")
    if ruta:
        return os.path.dirname(ruta)
    return None

def get_browser_cookies():
    navegadores = ["brave", "chrome", "edge", "firefox", "opera", "chromium"]
    for nav in navegadores:
        try:
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "cookiesfrombrowser": (nav,)
            }) as ydl:
                _ = ydl.cookiejar
            return (nav,)
        except Exception:
            continue
    return None

def construir_opciones(carpeta, calidad):
    opciones = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(carpeta, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": calidad,
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "writethumbnail": True,
        "quiet": False,
        "no_warnings": False,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web_safari", "tv"]
            }
        }
    }

    ffmpeg = get_ffmpeg_path()
    if ffmpeg:
        opciones["ffmpeg_location"] = ffmpeg

    if os.path.exists(COOKIE_FILE):
        opciones["cookiefile"] = COOKIE_FILE
    else:
        browser = get_browser_cookies()
        if browser:
            opciones["cookiesfrombrowser"] = browser

    return opciones

def descargar_mp3(url: str, carpeta: str = "./downloads", calidad: str = "0"):
    os.makedirs(carpeta, exist_ok=True)
    opciones = construir_opciones(carpeta, calidad)

    print(f"\nDescargando: {url}")
    print(f"Destino: {os.path.abspath(carpeta)}\n")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("\nDescarga completada!")
    except yt_dlp.utils.DownloadError as e:
        mensaje = str(e)
        if "Sign in to confirm you're not a bot" in mensaje:
            mensaje = (
                "YouTube bloqueo la descarga. "
                "La solucion mas estable es exportar cookies.txt desde tu navegador del PC "
                "y dejarlo en la carpeta del proyecto."
            )
        elif "429" in mensaje or "Too Many Requests" in mensaje:
            mensaje = (
                "YouTube esta limitando las solicitudes (429 Too Many Requests). "
                "Espera un rato o usa cookies.txt desde una sesion iniciada."
            )
        print(f"\nError al descargar: {mensaje}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Descarga MP3 desde YouTube y otros sitios usando yt-dlp"
    )
    parser.add_argument("url", help="URL del video o audio a descargar")
    parser.add_argument(
        "-o", "--output",
        default="./downloads",
        help="Carpeta de destino (default: ./downloads)",
    )
    parser.add_argument(
        "-q", "--quality",
        default="0",
        choices=["0", "128", "192", "256", "320"],
        help="Calidad del MP3 en kbps (0 = maxima, default: 0)",
    )

    args = parser.parse_args()
    descargar_mp3(args.url, args.output, args.quality)

if __name__ == "__main__":
    main()