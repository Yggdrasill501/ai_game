"""Module with game logic."""
import pygame
import random
from game.bird.bird import Bird
from game.pipe.pipe import Pipe
from game.button.button import Button
import game.settings as settings
import game.controls_hand as controls

class Game:
    def __init__(self) -> None:
        """Initialize game."""
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()
        self.flappy = Bird(100, settings.SCREEN_HEIGHT // 2)
        self.bird_group.add(self.flappy)
        self.button = Button(settings.SCREEN_WIDTH // 2 - 50, settings.SCREEN_HEIGHT // 2 - 100, settings.BUTTON_IMG)
        self.ground_scroll = 0
        self.score = 0
        self.pass_pipe = False
        self.last_pipe = pygame.time.get_ticks() - settings.PIPE_FREQUENCY
        self.flying = False
        self.game_over = False

    def check_collisions(self) -> None:
            """Check if the bird collides with pipes or the ground."""
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
                self.game_over = True
            if self.flappy.rect.bottom >= 768:
                self.game_over = True
                self.flying = False

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(settings.FPS)
            self.screen.blit(settings.BG, (0, 0))

            # Render PoseNet output
            settings.render_output()

            self.pipe_group.draw(self.screen)
            self.bird_group.draw(self.screen)
            self.bird_group.update()

            self.screen.blit(settings.GROUND_IMG, (self.ground_scroll, 768))

            if self.flying and not self.game_over:
                self.generate_pipes()
                self.pipe_group.update()
                self.update_ground()

            self.check_collisions()
            self.display_score()

            if self.game_over and controls.check_reset_button(self.button):
                self.game_over = False
                self.flying = False
                self.reset_game()

            # Handling user input via PoseNet or mouse
            for event in pygame.event.get():
                if controls.check_quit(event):
                    running = False
                if controls.check_start_flying(event, self.flying, self.game_over):
                    self.flying = True

            pygame.display.update()

        pygame.quit()

    def generate_pipes(self) -> None:
        """Generates pipes for the game."""
        time_now = pygame.time.get_ticks()
        if time_now - self.last_pipe > settings.PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT // 2 + pipe_height, -1)
            top_pipe = Pipe(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT // 2 + pipe_height, 1)
            self.pipe_group.add(btm_pipe)
            self.pipe_group.add(top_pipe)

    def display_score(self) -> None:
        """Displays the player's score on the screen."""
        font = pygame.font.SysFont('Bauhaus 93', 60)
        white = (255, 255, 255)
        score_text = font.render(str(self.score), True, white)
        self.screen.blit(score_text, (settings.SCREEN_WIDTH // 2, 20))
