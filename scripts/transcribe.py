# scripts/transcribe.py

import whisper
import os
import sys

def transcribe_file(input_file, output_dir="transcripts"):
    os.makedirs(output_dir, exist_ok=True)
    
    model = whisper.load_model("base")  # or "small", "medium", "large" as you expand
    print(f"Transcribing {input_file}...")

    result = model.transcribe(input_file)
    
    # Save as plain text transcript
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    txt_path = os.path.join(output_dir, base_filename + ".txt")
    with open(txt_path, "w") as f:
        f.write(str(result["text"]))

    # Save as JSON with segments & timestamps
    json_path = os.path.join(output_dir, base_filename + ".json")
    import json
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Transcript saved to {txt_path} and {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py path_to_input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    transcribe_file(input_file)
