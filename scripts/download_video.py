# scripts/download.py

import yt_dlp
import os

def download_video(url, output_dir="input"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=L95zgmbt2Zk&t=67s"
    download_video(test_url)
