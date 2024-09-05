"""Settings for the game Flappy Bird"""
import pygame

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
