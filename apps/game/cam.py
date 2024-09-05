import jetson_inference
import jetson_utils

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson_utils.videoSource("/dev/video0")  # using default camera
display = jetson_utils.videoOutput("display://0")

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img)
    display.Render(img)
    for detection in detections:
        print(f"Detected hand at ({detection.Center[0]}, {detection.Center[1]})")
