"""Settings for the game Flappy Bird"""
import pygame
import sys
import argparse
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

# Parse the command line arguments
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream (default is /dev/video0)")
parser.add_argument("output", type=str, default="display://0", nargs='?', help="URI of the output stream (default is display://0)")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (default is ssd-mobilenet-v2)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g., 'box,labels,conf')")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")

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
THRESHOLD_X_POSITION = 640

def process_detections(detections):
    """Process the detections and trigger in-game events if necessary."""
    for detection in detections:
        if detection.ClassID == RIGHT_HAND_LABEL_ID:
            hand_x_center = detection.Center[0]
            if hand_x_center > THRESHOLD_X_POSITION:

                print("Hand detected in the correct position, trigger jump")

# Screen settings
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Font
pygame.init()
FONT = pygame.font.SysFont('Bauhaus 93', 60)

# Game variables
GROUND_SCROLL = 0
SCROLL_SPEED = 4
FLYING = False
GAME_OVER = False
PIPE_GAP = 350
PIPE_FREQUENCY = 2000  # milliseconds

# Load images
BG = pygame.image.load('assets/bg.png')
GROUND_IMG = pygame.image.load('assets/ground.png')
BUTTON_IMG = pygame.image.load('assets/restart.png')
