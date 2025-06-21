# scripts/clip.py

import os
import json
import subprocess

def extract_clips(input_video, highlights_path, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(highlights_path, "r") as f:
        highlights = json.load(f)
    
    for idx, highlight in enumerate(highlights):
        start = highlight["start"]
        end = highlight["end"]
        duration = end - start
        output_filename = f"highlight_{idx+1:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        cmd = [
            "ffmpeg",
            "-y",  # overwrite output file if exists
            "-i", input_video,
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",
            output_path
        ]

        print(f"Extracting clip: {output_filename} ({start} - {end})")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Clipping complete.")

if __name__ == "__main__":
    # Fill these with your actual files:
    input_video = "input/test_video.mkv"
    highlights_path = "clips/highlights.json"

    extract_clips(input_video, highlights_path)
