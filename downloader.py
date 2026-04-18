# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import os
import shutil
import sys

try:
    import yt_dlp
except ImportError:
    print("yt-dlp no esta instalado. Ejecuta: pip install yt-dlp")
    sys.exit(1)

def get_ffmpeg_path():
    ruta = shutil.which("ffmpeg")
    if ruta:
        return os.path.dirname(ruta)
    return None

def descargar_mp3(url: str, carpeta: str = "./downloads", calidad: str = "0"):
    os.makedirs(carpeta, exist_ok=True)

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
    }

    ffmpeg = get_ffmpeg_path()
    if ffmpeg:
        opciones["ffmpeg_location"] = ffmpeg

    print(f"\nDescargando: {url}")
    print(f"Destino: {os.path.abspath(carpeta)}\n")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("\nDescarga completada!")
    except yt_dlp.utils.DownloadError as e:
        print(f"\nError al descargar: {e}")
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
