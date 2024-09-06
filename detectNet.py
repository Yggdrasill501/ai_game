#!/usr/bin/env python3
import sys
import argparse
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log, cudaDrawRect

parser = argparse.ArgumentParser(description="Detect right-hand movement using an object detection DNN.",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream (default: /dev/video0)")
parser.add_argument("output", type=str, default="display://0", nargs='?', help="URI of the output stream (default: display://0)")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="Pre-trained model to load (default: ssd-mobilenet-v2)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="Detection overlay flags (e.g., --overlay=box,labels,conf)")
parser.add_argument("--threshold", type=float, default=0.5, help="Minimum detection threshold to use")

try:
    args = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)

net = detectNet(args.network, sys.argv, args.threshold)

RIGHT_HAND_LABEL_ID = 1

while True:
    img = input.Capture()

    if img is None:
        continue

    detections = net.Detect(img, overlay=args.overlay)

    print(f"Detected {len(detections)} objects in image")

    for detection in detections:
        if detection.ClassID == RIGHT_HAND_LABEL_ID:
            print(f"Detected right hand (person): {detection}")

            cudaDrawRect(img, (detection.Left, detection.Top, detection.Right, detection.Bottom), color=(0, 0, 255, 100))

    output.Render(img)

    output.SetStatus(f"{args.network} | Network {net.GetNetworkFPS():.0f} FPS")

    net.PrintProfilerTimes()

    if not input.IsStreaming() or not output.IsStreaming():
        break
