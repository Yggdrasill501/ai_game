"""This module contains functions to control the game using hand gestures."""
from game.button.button import Button
import pygame
import sys
import jetson_utils
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, cudaDrawRect

# Set up the detectNet network using the default model and parameters
net = detectNet("ssd-mobilenet-v2", sys.argv, 0.5)

# Set up the video input source (camera) and output (optional)
input = videoSource("/dev/video0", argv=sys.argv)  # Change the input as necessary
output = videoOutput()  # Optional, leave empty if no output rendering is required

# Define the right-hand label ID for the object you want to detect (replace with actual label)
RIGHT_HAND_LABEL_ID = YOUR_HAND_LABEL_ID  # Adjust this with the correct label ID

def check_right_hand_movement() -> bool:
    """Use detectNet to check for right hand movement and draw bounding box."""

    # Capture the next image from the camera
    img = input.Capture()

    if img is None:  # timeout
        print("[ERROR] Timeout waiting for image buffer")
        return False

    # Detect objects in the image
    detections = net.Detect(img)

    # Loop through detections to find the right hand (assuming label ID for the hand is known)
    for detection in detections:
        if detection.ClassID == RIGHT_HAND_LABEL_ID:
            # Draw a bounding box around the detected right hand
            cudaDrawRect(img, (detection.Left, detection.Top, detection.Right, detection.Bottom), color=(0, 0, 255, 100))

            # Use the position of the hand to control the bird
            hand_x_center = detection.Center[0]

            # Assuming you want the bird to jump if the hand is above a certain X threshold
            if hand_x_center > THRESHOLD_X_POSITION:  # set your threshold based on the game's layout
                return True

    # Render the output if necessary (optional)
    output.Render(img)

    return False  # No right hand detected or it was outside the threshold


def check_quit(event: pygame.event.Event) -> bool:
    """Check if the user wants to quit the game.

    :param event: The pygame event to check.
    :return: True if the user wants to quit, False otherwise.
    """
    if event.type == pygame.QUIT:
        return True
    return False


def check_jump() -> bool:
    """Check if the bird should jump (based on right-hand detection or mouse press)."""
    return check_right_hand_movement() or pygame.mouse.get_pressed()[0] == 1


def check_start_flying(event: pygame.event.Event, flying: bool, game_over: bool) -> bool:
    """Check if the game should start flying (detect right hand or mouse click).

    :param event: pygame.event.Event, pygame event to check.
    :param flying: bool, indicating if the bird is currently flying.
    :param game_over: bool, indicating if the game is over.
    :return: True if the game should start flying, False otherwise.
    """
    if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
        return True
    if check_right_hand_movement() and not flying and not game_over:
        return True
    return False


def check_reset_button(button: Button) -> bool:
    """Check if the reset button is clicked.

    :param button: Button, the reset button to check.
    """
    return button.draw(pygame.display.get_surface())
