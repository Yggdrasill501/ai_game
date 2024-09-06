#!/usr/bin/env python3

import sys
import argparse
from jetson_inference import poseNet
from jetson_utils import videoSource, videoOutput, cudaDrawCircle, Log

# Parse the command line
parser = argparse.ArgumentParser(description="Detect hand movement using PoseNet for human pose estimation.",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=poseNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream (default: /dev/video0)")
parser.add_argument("output", type=str, default="display://0", nargs='?', help="URI of the output stream (default: display://0)")
parser.add_argument("--network", type=str, default="resnet18-body", help="Pre-trained model to load (default: resnet18-body)")
parser.add_argument("--overlay", type=str, default="links,keypoints", help="PoseNet overlay flags (e.g., 'links,keypoints')")
parser.add_argument("--threshold", type=float, default=0.15, help="Minimum detection threshold to use")

try:
    args = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# Create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)

# Load the PoseNet network
net = poseNet(args.network, sys.argv, args.threshold)

# COCO keypoint index for right wrist
RIGHT_WRIST_ID = 4  # PoseNet keypoint ID for the right wrist (based on COCO)

# Process frames until EOS or the user exits
while True:
    # Capture the next image
    img = input.Capture()

    if img is None:  # Timeout
        continue

    # Perform pose estimation on the image
    poses = net.Process(img, overlay=args.overlay)

    # Print the number of detected poses
    print(f"Detected {len(poses)} poses")

    # Loop through each detected pose
    for pose in poses:
        # Check if the right wrist keypoint is detected
        keypoint = pose.Keypoints[RIGHT_WRIST_ID]

        if keypoint.Confidence > args.threshold:
            print(f"Right wrist detected at ({keypoint.X}, {keypoint.Y}) with confidence {keypoint.Confidence:.2f}")

            # Draw a circle at the right wrist
            cudaDrawCircle(img, (keypoint.X, keypoint.Y), 10, (255, 0, 0, 200))

    # Render the image
    output.Render(img)

    # Update the title bar with network performance
    output.SetStatus(f"{args.network} | Network {net.GetNetworkFPS():.0f} FPS")

    # Print out performance info
    net.PrintProfilerTimes()

    # Exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
