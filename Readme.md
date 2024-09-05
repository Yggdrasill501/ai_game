# Flappy Bird with Hand Gesture Control

This is a modified version of the classic Flappy Bird game, where the bird is controlled using hand gesture detection. The detection is powered by NVIDIA Jetson Nano using the `detectNet` model from the `jetson-inference` library. The camera captures hand movements, and the game responds by making the bird "jump" based on the position of your hand.

## Requirements

To run this project, you need the following:

- **Hardware**: 
  - NVIDIA Jetson Nano or any Jetson device with CUDA support
  - Camera (connected to `/dev/video0`)
  
- **Software**:
  - Python 3.6+
  - Pygame 2.6.0
  - NVIDIA Jetson Inference libraries
  - GStreamer 1.20.3 or higher

### Required Python Packages

Make sure you have the following Python packages installed:
```bash
pip3 install pygame
```

### Jetson Libraries Setup

Ensure that the Jetson Inference library is properly installed. Follow the instructions from the official NVIDIA repository:

- [jetson-inference library installation](https://github.com/dusty-nv/jetson-inference)

## Installation

1. Clone the repository and navigate into the project directory:

```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Ensure your camera is connected and recognized at `/dev/video0`. You can check if the camera is connected by running:

```bash
ls /dev/video0
```

If it doesn’t show, check your camera connection and permissions.

3. Grant permissions to access the camera device:

```bash
sudo chmod 777 /dev/video0
```

4. Ensure you have the necessary dependencies installed (Jetson libraries, Pygame, etc.).

5. Modify the `settings.py` file to suit your configuration if necessary (e.g., camera resolution, detection model).

## Running the Game

Once the setup is complete, you can start the game:

```bash
python3 main.py
```

## Game Controls

- **Hand Gesture Control**: Raise your hand in front of the camera to make the bird jump.
- **Mouse Click**: Alternatively, you can use the left mouse button to control the bird.
- **Restart Game**: After the game is over, click the restart button to play again.
