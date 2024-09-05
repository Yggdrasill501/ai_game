"""Module conrols for game controls."""
import pygame
from button.button import Button

def check_quit(event: pygame.event) -> bool:
    """Check if the user wants to quit the game.
    :param event: pygame.evet, pygame event.
    :returns: bool, quit.
    """
    if event.type == pygame.QUIT:
        return True
    return False

def check_start_flying(event: pygame.event, flying: bool, game_over: bool) -> bool:
    """Check if the game should start flying (mouse or key press).
    :param event: pygame.evet, pygame event.
    :param flying: bool, flying.
    :param game_over: bool, game over.
    :returns: bool, start flying.
    """
    if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
        return True
    return False

def check_jump() -> bool:
    """Check if the bird should jump (mouse press)."""
    return pygame.mouse.get_pressed()[0] == 1

def check_reset_button(button: Button) -> bool:
    """Check if the reset button is clicked.

    :param button: Button, button.
    :returns: bool, action.
    """
    return button.draw(pygame.display.get_surface())
