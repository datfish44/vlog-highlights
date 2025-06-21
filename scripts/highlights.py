# scripts/highlights.py

import os
import json

HIGHLIGHT_KEYWORDS = [
    "oh my god", "wow", "crazy", "amazing", "beautiful", 
    "first time", "shrine", "onsen", "ramen", "bento", "japan", "so cute"
]

BUFFER_SECONDS = 5  # add 5 seconds before and after for context

def extract_highlights(transcript_path, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(transcript_path, "r") as f:
        transcript = json.load(f)

    highlights = []

    for segment in transcript["segments"]:
        text = segment["text"].lower()

        if any(keyword in text for keyword in HIGHLIGHT_KEYWORDS):
            start_time = max(0, segment["start"] - BUFFER_SECONDS)
            end_time = segment["end"] + BUFFER_SECONDS
            highlights.append({
                "start": start_time,
                "end": end_time,
                "text": segment["text"]
            })

    # Save highlight timestamps to JSON for the next step (clipping)
    highlights_path = os.path.join(output_dir, "highlights.json")
    with open(highlights_path, "w") as f:
        json.dump(highlights, f, indent=2)

    print(f"Found {len(highlights)} highlights.")
    print(f"Saved highlight timestamps to {highlights_path}")

if __name__ == "__main__":
    transcript_file = "transcripts/test_video.json"  # <-- put your actual transcript file here
    extract_highlights(transcript_file)
