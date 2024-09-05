"""Settings for the game Flappy Bird"""
import pygame
import sys
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

input = videoSource("/dev/video0", argv=[
    '--input-width=640',
    '--input-height=480',
    '--framerate=30'
])
output = videoOutput()  # Leave empty if no output rendering is required

MODEL_NAME = "ssd-mobilenet-v2"
THRESHOLD = 0.5
net = detectNet(MODEL_NAME, sys.argv, THRESHOLD)

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
