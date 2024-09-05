""""Hand detection-based controls for the Flappy Bird game."""
import pygame
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
from game.button.button import Button

# Set up the detectNet network
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
input = videoSource("/dev/video0")  # Assuming you are using the Jetson Nano camera input
output = videoOutput()  # Optionally stream to display/output

def check_quit(event: pygame.event) -> bool:
    """Check if the user wants to quit the game.

    :param event: pygame.event, pygame event.
    :returns: bool, quit.
    """
    if event.type == pygame.QUIT:
        return True
    return False

def check_right_hand_movement():
    """Use detectNet to check for right hand movement."""
    img = input.Capture()

    if img is None:
        print("[ERROR] Timeout waiting for image buffer")
        return False  # Return false if no image is captured, skip processing

    detections = net.Detect(img)

    for detection in detections:
        if detection.ClassID == YOUR_HAND_LABEL_ID:  # replace with actual hand class ID
            hand_x_center = detection.Center[0]

            if hand_x_center > THRESHOLD_X_POSITION:  # set a threshold based on your needs
                return True

    output.Render(img)

    return False

    # Detect objects in the image
    detections = net.Detect(img)

    # Loop through detections to find the right hand (assuming label ID for hand is known)
    for detection in detections:
        # Assuming that the right-hand object class has a specific ID (use appropriate label for your network)
        # You can identify it by printing `detection.ClassID` and mapping it
        if detection.ClassID == YOUR_HAND_LABEL_ID:  # replace with actual hand class ID
            # Use the position of the hand to control the bird
            hand_x_center = detection.Center[0]

            # Assuming you want the bird to jump if the hand is above a certain point
            if hand_x_center > THRESHOLD_X_POSITION:  # set a threshold based on your needs
                return True

    # Render the output (optional, can be removed if not needed)
    output.Render(img)

    return False

def check_jump() -> bool:
    """Check if the bird should jump (based on right hand detection or mouse).

    :returns: bool, jump.
    """
    # Use hand detection as a jump trigger
    return check_right_hand_movement() or pygame.mouse.get_pressed()[0] == 1

def check_start_flying(event: pygame.event, flying: bool, game_over: bool) -> bool:
    """Check if the game should start flying (detect right hand or mouse click).

    :param event: pygame.event, pygame event.
    :param flying: bool, flying.
    :param game_over: bool, game over.
    :returns: bool, start flying.
    """
    # Check for right hand movement or mouse press to start the game
    if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
        return True
    if check_right_hand_movement() and not flying and not game_over:
        return True
    return False

def check_reset_button(button: Button) -> bool:
    """Check if the reset button is clicked.

    :param button: Button, button.
    :returns: bool, action.
    """
    return button.draw(pygame.display.get_surface())
