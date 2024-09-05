from detect_net import DetectNet
from game_logic import Game

fn main():
    # Initialize game settings
    game = Game()

    # Initialize detectNet for hand detection using the GPU
    detect_net = DetectNet(model_path="ssd_mobilenet_v2", input_device="/dev/video0")

    # Start the game loop
    while not game.is_over:
        # Capture hand detection result
        hand_detected = detect_net.detect_hand()

        # Update game state based on hand movement
        game.update(hand_detected)

        # Render the game
        game.render()

    print("Game Over")

if __name__ == "__main__":
    main()
