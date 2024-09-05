"""This module contains functions to control the game using hand gestures."""
from game.button import Button
import pygame
import sys
import jetson_utils
from jetson_utils import cudaDrawRect
import game.settings as settings

def check_right_hand_movement() -> bool:
    """Use detectNet to check for right hand movement and draw bounding box."""

    # Capture the next image from the camera
    img = settings.input.Capture()

    if img is None:  # timeout
        print("[ERROR] Timeout waiting for image buffer")
        return False

    # Detect objects in the image using the detectNet model
    detections = settings.net.Detect(img)

    # Loop through detections to find the right hand (assuming label ID for the hand is known)
    for detection in detections:
        if detection.ClassID == settings.RIGHT_HAND_LABEL_ID:
            # Draw a bounding box around the detected right hand
            cudaDrawRect(img, (detection.Left, detection.Top, detection.Right, detection.Bottom), color=(0, 0, 255, 100))

            # Use the position of the hand to control the bird
            hand_x_center = detection.Center[0]

            # Assuming you want the bird to jump if the hand is above a certain X threshold
            if hand_x_center > settings.THRESHOLD_X_POSITION:  # using the threshold from settings
                return True

    # Render the output if necessary (optional)
    settings.output.Render(img)

    return False  # No right hand detected or it was outside the threshold


def check_quit(event: pygame.event.Event) -> bool:
    """Check if the user wants to quit the game.

    :param event: pygame.event.Event, pygame event to check
    :returns: True if the user wants to quit, False otherwise
    """
    if event.type == pygame.QUIT:
        return True
    return False


def check_jump() -> bool:
    """Check if the bird should jump (based on right-hand detection or mouse press)."""
    return check_right_hand_movement() or pygame.mouse.get_pressed()[0] == 1


def check_start_flying(event: pygame.event.Event, flying: bool, game_over: bool) -> bool:
    """Check if the game should start flying (detect right hand or mouse click).

    :param event: pygame.event.Event, pygame event to check
    :param flying: bool, whether the bird is flying
    :param game_over: bool, whether the game is over
    :returns: True if the game should start flying, False otherwise
    """
    if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
        return True
    if check_right_hand_movement() and not flying and not game_over:
        return True
    return False


def check_reset_button(button: Button) -> bool:
    """Check if the reset button is clicked.

    :param button: Button, button to check
    :returns: True if the button is clicked, False otherwise
    """
    return button.draw(pygame.display.get_surface())
