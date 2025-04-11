import cv2
import os
from models.image_model import detect_image_fake

def extract_frames(video_path, max_frames=5):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(total_frames // max_frames, 1)
    
    frames = []
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret or len(frames) >= max_frames:
            break
        if count % frame_interval == 0:
            frame_path = f"temp_frame_{count}.jpg"
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
        count += 1
    cap.release()
    return frames

def detect_video_fake(filepath):
    frame_paths = extract_frames(filepath)
    scores = []
    for frame in frame_paths:
        score, _ = detect_image_fake(frame)
        scores.append(score)
        os.remove(frame)

    avg_score = round(sum(scores) / len(scores), 2)
    explanation = f"Average frame-based deepfake confidence: {avg_score}%, over {len(scores)} frames."
    return avg_score, explanation
