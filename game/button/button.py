"""Package for button to restart game."""
import pygame

class Button:
    """Button to restart game."""""

    def __init__(self, x: int, y: int, image: str) -> None:
        """Initialize.
        :param x: int, x position.
        :param y: int, y position.
        :param image: str, image path.
        :returns: None.
        """
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen) -> bool:
        """"Draw button.

        :param screen: pygame.Surface, screen to draw on.
        :returns: bool, action.
        """
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
