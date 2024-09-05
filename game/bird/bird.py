"""Module with bird sprite."""
import pygame
from game.settings import GAME_OVER, FLYING

class Bird(pygame.sprite.Sprite):
    """Sprite brid."""

    def __init__(self, x: int, y: int) -> None:
        """Ininitialize.

        :param x: int, rect x position.
        :param y: int, rect y position.
        :returns: None.
        """
        super().__init__()
        self.images = [pygame.image.load(f'assets/bird{num}.png') for num in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False

    def update(self) -> None:
        """Update bird."""
        if FLYING:
            self.vel += 0.5
            self.vel = min(self.vel, 8)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not GAME_OVER:
            self.handle_jump()
            self.animate()
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

    def handle_jump(self)-> None:
        """Handle jump."""
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def animate(self) -> None:
        """Animate bird."""
        self.counter += 1
        if self.counter > 5:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
