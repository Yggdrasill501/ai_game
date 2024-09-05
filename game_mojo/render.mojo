struct Renderer:
    screen_width: Int
    screen_height: Int

    fn __init__(self, screen_width: Int, screen_height: Int):
        self.screen_width = screen_width
        self.screen_height = screen_height

    fn render_game(self, bird_y: Float, score: Int):
        print(f"Rendering bird at y: {bird_y} with score: {score}")
