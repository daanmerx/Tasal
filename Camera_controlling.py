import cv2
import os
from datetime import datetime

def take_photo(save_path, camera_index=1):
    """
    Maak direct één foto met de camera en sla deze op in save_path.
    """
    # Open camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("Kan de camera niet openen. Controleer de aansluiting of het indexnummer.")

    # Zorg dat de map bestaat
    os.makedirs(save_path, exist_ok=True)

    # Lees één frame
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Geen frame ontvangen van de camera.")

    # Genereer bestandsnaam en sla op
    bestandsnaam = datetime.now().strftime("foto_%Y%m%d_%H%M%S.png")
    bestandspad = os.path.join(save_path, bestandsnaam)
    if cv2.imwrite(bestandspad, frame):
        print(f"✅ Foto opgeslagen als: {bestandspad}")
