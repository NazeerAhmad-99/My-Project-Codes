import cv2
import os
import time
import json
import threading
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open the camera.")

# Settings for data capture
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLES_PER_PERSON = 20
CAPTURE_DELAY_SEC = 0.2
MODEL_PATH = os.path.join(BASE_DIR, "trainer.yml")
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")
CONFIDENCE_THRESHOLD = 65

os.makedirs(DATA_DIR, exist_ok=True)

print("Controls:")
print("  Use the GUI window to set name and start/stop capture")
print("  q = quit (camera window)")

def load_training_data(data_dir):
    images = []
    labels = []
    label_map = {}
    current_id = 0

    for person in sorted(os.listdir(data_dir)):
        person_dir = os.path.join(data_dir, person)
        if not os.path.isdir(person_dir):
            continue

        label_map[current_id] = person

        for filename in os.listdir(person_dir):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            path = os.path.join(person_dir, filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            images.append(img)
            labels.append(current_id)
        current_id += 1
    return images, np.array(labels), label_map

def show_error_and_exit(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Face App Error", message)
    root.destroy()
    raise SystemExit(1)

recognizer = cv2.face.LBPHFaceRecognizer_create()

if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
    recognizer.read(MODEL_PATH)
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels_map = json.load(f)
    # JSON keys are strings; convert to int for lookup consistency
    labels_map = {int(k): v for k, v in labels_map.items()}
    print(f"Loaded existing model from {MODEL_PATH}.")
else:
    print("Training recogniser...")
    train_images, train_labels, labels_map = load_training_data(DATA_DIR)

    if len(train_images) == 0:
        show_error_and_exit(
            "No training data found.\n"
            "Capture samples first, then click Retrain."
        )

    recognizer.train(train_images, train_labels)
    recognizer.save(MODEL_PATH)

    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(labels_map, f)
    print(f"Training completed and model is saved to {MODEL_PATH}.")

# ---- Simple GUI for name entry and capture control ----
current_name = None
saved_count = 0
last_save_time = 0.0

ui_name = ""
set_name_requested = False
capture_enabled = False
exit_requested = False
retrain_requested = False

def gui_thread():
    global ui_name, set_name_requested, capture_enabled, exit_requested, retrain_requested

    root = tk.Tk()
    root.title("Face Capture Controls")
    root.geometry("380x230")

    tk.Label(root, text="Person Name:").pack(pady=(10, 0))
    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=5)

    def on_set_name():
        global ui_name, set_name_requested
        name = name_entry.get().strip()
        if name:
            ui_name = name
            set_name_requested = True

    def on_start():
        global capture_enabled
        capture_enabled = True

    def on_stop():
        global capture_enabled
        capture_enabled = False

    def on_quit():
        global exit_requested
        exit_requested = True
        root.quit()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Set Name", width=10, command=on_set_name).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Start Capture", width=12, command=on_start).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Stop Capture", width=12, command=on_stop).grid(row=0, column=2, padx=5)

    def on_retrain():
        global retrain_requested
        retrain_requested = True

    status_var = tk.StringVar(value="Status: Idle")
    tk.Label(root, textvariable=status_var).pack(pady=(5, 0))

    tk.Button(root, text="Retrain", width=10, command=on_retrain).pack(pady=(5, 0))
    tk.Button(root, text="Quit", width=10, command=on_quit).pack(pady=(5, 0))

    def update_status():
        if exit_requested:
            return
        capture_state = "ON" if capture_enabled else "OFF"
        name_state = current_name if current_name else "None"
        status_var.set(f"Status: Capture {capture_state} | Name: {name_state} | Saved: {saved_count}")
        root.after(200, update_status)

    update_status()

    root.mainloop()

threading.Thread(target=gui_thread, daemon=True).start()

while True:
    if exit_requested:
        break

    ret, frame = cap.read()
    if not ret:
        print("Failed to read a frame from the camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # Recognize each detected face and draw name + box
    for (x, y, w, h) in faces:
        face_gray = gray[y:y + h, x:x + w]
        face_gray = cv2.resize(face_gray, (200, 200))

        label_id, confidence = recognizer.predict(face_gray)
        if confidence <= CONFIDENCE_THRESHOLD:
            name = labels_map.get(label_id, "Unknown")
        else:
            name = "Unknown"

        # Draw green box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw name above the box
        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    status = "Use GUI to set name and capture"
    if current_name:
        status = f"Name: {current_name} | Saved: {saved_count}/{SAMPLES_PER_PERSON}"

    cv2.putText(
        frame,
        status,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Live Camera", frame)

    # Press 'q' to quit the window.
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    # Retrain request from GUI
    if retrain_requested:
        print("Retraining recogniser...")
        train_images, train_labels, labels_map = load_training_data(DATA_DIR)
        if len(train_images) == 0:
            print("No training data found; retrain skipped.")
        else:
            recognizer.train(train_images, train_labels)
            recognizer.save(MODEL_PATH)
            with open(LABELS_PATH, "w", encoding="utf-8") as f:
                json.dump(labels_map, f)
            print("Retrain complete.")
        retrain_requested = False

    # Apply name from GUI
    if set_name_requested:
        current_name = ui_name
        person_dir = os.path.join(DATA_DIR, current_name)
        os.makedirs(person_dir, exist_ok=True)
        saved_count = 0
        set_name_requested = False
        print(f"Now capturing samples for {current_name}")

    # Capturing samples
    if capture_enabled and current_name and len(faces) > 0:
        now = time.time()
        if now - last_save_time >= CAPTURE_DELAY_SEC:
            # Save the biggest detected face
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            face_crop = frame[y:y + h, x:x + w]

            filename = f"{saved_count:03d}.jpg"
            filepath = os.path.join(DATA_DIR, current_name, filename)
            cv2.imwrite(filepath, face_crop)

            saved_count += 1
            last_save_time = now
            print(f"Saved {filepath}")

            if saved_count >= SAMPLES_PER_PERSON:
                print(f"Done capturing samples for {current_name}")
                current_name = None

cap.release()
cv2.destroyAllWindows()
