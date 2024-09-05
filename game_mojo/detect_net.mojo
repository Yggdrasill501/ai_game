from jetson_utils import videoSource, detectNet

struct DetectNet:
    model: detectNet
    camera: videoSource

    fn __init__(self, model_path: str, input_device: str):
        self.model = detectNet(model_path)
        self.camera = videoSource(input_device)

    fn detect_hand(self) -> Bool:
        img = self.camera.Capture()

        if img is None:
            print("Camera capture failed!")
            return False

        detections = self.model.Detect(img)

        for detection in detections:
            if detection.ClassID == 1:
                return True  # Hand detected

        return False
