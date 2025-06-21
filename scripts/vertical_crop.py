import os
import subprocess
import cv2
import numpy as np

# --------------------------------------------------------------------------------------
# vertical_crop.py — smart 16:9 ➔ 9:16 converter for YouTube Shorts
# --------------------------------------------------------------------------------------
# ✦ Strategy
#   1.  Face‑scan a few frames to estimate the subject’s horizontal position.
#   2.  Crop a 9:16 window that keeps the face roughly in the centre.
#   3.  Scale → 1080×1920 so it uploads cleanly as a Short.
#
#   Note:  With a full‑height crop you can NEVER reveal more than ~60 % of the
#   original width (1080 px tall → 607 px wide).  That’s just how 9:16 works.
#   “Zooming out” beyond that would require adding letter‑boxes, not cropping.
# --------------------------------------------------------------------------------------


def detect_faces(video_path: str, every_n_frames: int = 45) -> list[int]:
    """Return x‑coords of the biggest face in every *every_n_frames* frame."""
    detector = cv2.CascadeClassifier(cv2.__path__[0] + "/data/haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(video_path)
    xs: list[int] = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % every_n_frames == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.1, 4)
            if len(faces):
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                xs.append(x + w // 2)
            else:
                xs.append(frame.shape[1] // 2)
        idx += 1
    cap.release()
    return xs


def pick_crop_x(face_centres: list[int], frame_w: int, crop_w: int) -> int:
    """Centre the crop on the median face location; keep inside the frame."""
    if not face_centres:
        return (frame_w - crop_w) // 2
    median = int(np.median(face_centres))
    return int(np.clip(median - crop_w // 2, 0, frame_w - crop_w))


def convert_to_shorts(src: str, dst_dir: str = "output") -> None:
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))

    cap = cv2.VideoCapture(src)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    # If the clip is already vertical, just centre‑crop to 9:16 and resize.
    if h > w:
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        subprocess.run(["ffmpeg", "-y", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "copy", dst], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[vertical_crop] portrait passthrough → {dst}")
        return

    # Landscape → find face → crop full height, 9:16 width ≈ 0.5625 × h.
    print(f"[vertical_crop] scanning faces → {os.path.basename(src)} …")
    faces = detect_faces(src)

    crop_w = int(round(h * 9 / 16))
    crop_x = pick_crop_x(faces, w, crop_w)

    vf = f"crop={crop_w}:{h}:{crop_x}:0,scale=1080:1920"

    subprocess.run(["ffmpeg", "-y", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "copy", dst], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[vertical_crop] crop {crop_w}×{h} at x={crop_x} → {dst}")


if __name__ == "__main__":
    CLIP_DIR = "clips"
    for f in os.listdir(CLIP_DIR):
        if f.lower().endswith(".mp4"):
            convert_to_shorts(os.path.join(CLIP_DIR, f))
