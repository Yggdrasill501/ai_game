import pygame
import jetson_inference
import jetson_utils

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
player = pygame.Rect(375, 275, 50, 50)

# Set up hand detection
net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson_utils.videoSource("/dev/video0")
running = True

while running:
    # Capture frame and detect hands
    img = camera.Capture()
    detections = net.Detect(img)

    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if a hand is detected and move the player
    for detection in detections:
        hand_x, hand_y = detection.Center
        # Normalize hand position for screen resolution
        screen_width, screen_height = screen.get_size()
        normalized_x = int(hand_x * (screen_width / img.width))
        normalized_y = int(hand_y * (screen_height / img.height))

        # Move player based on hand position
        player.center = (normalized_x, normalized_y)

    # Draw the game scene
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, (255, 0, 0), player)  # Draw the player

    pygame.display.flip()

pygame.quit()
