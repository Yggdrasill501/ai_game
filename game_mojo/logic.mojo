struct Game:
    bird_y: Float
    bird_velocity: Float
    gravity: Float
    is_over: Bool
    score: Int

    fn __init__(self):
        self.bird_y = 300.0
        self.bird_velocity = 0.0
        self.gravity = 0.5
        self.is_over = False
        self.score = 0

    fn update(self, hand_detected: Bool):
        # Apply gravity to the bird
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        if hand_detected:
            self.bird_velocity = -10.0

        if self.bird_y <= 0 or self.bird_y >= 720:  # Assuming screen height of 720
            self.is_over = True

    fn render(self):
        print(f"Rendering bird at position: {self.bird_y}, score: {self.score}")
