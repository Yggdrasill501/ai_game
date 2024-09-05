from detect_net import DetectNet
from game_logic import Game
from renderer import Renderer
from settings import Settings

fn main():
    settings = Settings()

    game = Game()
    renderer = Renderer(screen_width=settings.screen_width, screen_height=settings.screen_height)
    detect_net = DetectNet(model_path="ssd_mobilenet_v2", input_device="/dev/video0")

    while not game.is_over:
        hand_detected = detect_net.detect_hand()

        game.update(hand_detected)

        renderer.render_game(bird_y=game.bird_y, score=game.score)

    print("Game Over")

if __name__ == "__main__":
    main()
