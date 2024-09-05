"""This module contains functions to control the game using hand gestures."""
from game.button.button import Button
import pygame
import sys
import jetson_utils
from jetson_utils import cudaDrawRect
import game.settings as settings

def check_right_hand_movement() -> bool:
    """Use detectNet to check for right hand movement and draw bounding box."""

    img = settings.input.Capture()
    if img is None:  # timeout
        print("[ERROR] Timeout waiting for image buffer")
        return False

    detections = settings.net.Detect(img)

    for detection in detections:
        if detection.ClassID == settings.RIGHT_HAND_LABEL_ID:
            cudaDrawRect(img, (detection.Left, detection.Top, detection.Right, detection.Bottom), color=(0, 0, 255, 100))

            hand_x_center = detection.Center[0]

            if hand_x_center > settings.THRESHOLD_X_POSITION:
                return True

    settings.output.Render(img)

    return False


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
    return settings.process_detections

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
