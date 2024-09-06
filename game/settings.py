"""Settings for the game Flappy Bird"""
import pygame
import sys
import argparse
from jetson_inference import poseNet
from jetson_utils import videoSource, videoOutput, Log

# Create video sources and outputs
input = videoSource("/dev/video0", argv=sys.argv)
output = videoOutput("display://0", argv=sys.argv)

# Initialize the PoseNet model
net = poseNet("resnet18-body", sys.argv, 0.15)

# COCO keypoint index for the right wrist
RIGHT_WRIST_ID = 4  # Keypoint index for the right wrist
movement_threshold = 10  # Movement threshold in pixels

# Variables to track right wrist movement
previous_wrist_position = None

def detect_right_hand_movement(current_wrist, previous_wrist):
    """Detect if the right hand is moving by comparing the current and previous wrist positions."""
    if previous_wrist is None:
        return False  # No movement detected in the first frame

    # Calculate the Euclidean distance between the two wrist positions
    distance = ((current_wrist[0] - previous_wrist[0]) ** 2 + (current_wrist[1] - previous_wrist[1]) ** 2) ** 0.5

    # Return True if the movement exceeds the threshold
    return distance > movement_threshold

def check_right_hand_movement():
    """Check if the right hand is moving by detecting wrist movement using PoseNet."""
    global previous_wrist_position

    # Capture the next image from the camera
    img = input.Capture()

    if img is None:  # Timeout
        return False

    # Perform pose estimation
    poses = net.Process(img, overlay="links,keypoints")

    # Initialize the current wrist position
    current_wrist_position = None

    # Loop through detected poses and check for the right wrist
    for pose in poses:
        keypoint = pose.Keypoints[RIGHT_WRIST_ID]
        if keypoint.Confidence > 0.15:
            current_wrist_position = (keypoint.X, keypoint.Y)
            # Draw a circle around the right wrist
            cudaDrawCircle(img, (keypoint.X, keypoint.Y), 10, (255, 0, 0, 200))

    # If the wrist position is detected, check for movement
    if current_wrist_position:
        is_moving = detect_right_hand_movement(current_wrist_position, previous_wrist_position)
        previous_wrist_position = current_wrist_position  # Update wrist position
        return is_moving

    return False  # No wrist detected

# Render the output (this can be called in the game loop to render the video)
# def render_output():
#    output.Render(input.Capture())


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
