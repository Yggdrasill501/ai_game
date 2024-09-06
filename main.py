"""Module main."""
from game.game import Game
import threading
import game.settings as settings


def capture_camera_frames() -> None:
    """Capture camera frames and run object detection."""
    while True:
        img = settings.input.Capture()

        if img is None:
            print("[ERROR] Timeout waiting for image buffer")
            continue

        detections = settings.net.Detect(img)
        settings.process_detections(detections)

        settings.output.Render(img)

threading.Thread(target=capture_camera_frames, daemon=True).start()

if __name__ == "__main__":
    game = Game()
    game.run()
