import pyboy
import os
from PIL import Image

# Load the ROM file
gameboy = pyboy.PyBoy("rom.gb")
gameboy.set_emulation_speed(0)

# Load the frame
frameImage = Image.open("vetlendo.png")

# Load state
try:
    with open("state_file.state", "rb") as file:
        gameboy.load_state(file)
except Exception as e:
    print("Creating new save")

# Set input
issueTitle = os.environ["ISSUE_TITLE"]
buttonPresses = {
    "A":pyboy.WindowEvent.PRESS_BUTTON_A,
    "B":pyboy.WindowEvent.PRESS_BUTTON_B,
    "START":pyboy.WindowEvent.PRESS_BUTTON_START,
    "SELECT":pyboy.WindowEvent.PRESS_BUTTON_SELECT,
    "UP":pyboy.WindowEvent.PRESS_ARROW_UP,
    "DOWN":pyboy.WindowEvent.PRESS_ARROW_DOWN,
    "LEFT":pyboy.WindowEvent.PRESS_ARROW_LEFT,
    "RIGHT":pyboy.WindowEvent.PRESS_ARROW_RIGHT
}
buttonReleases = {
    "A":pyboy.WindowEvent.RELEASE_BUTTON_A,
    "B":pyboy.WindowEvent.RELEASE_BUTTON_B,
    "START":pyboy.WindowEvent.RELEASE_BUTTON_START,
    "SELECT":pyboy.WindowEvent.RELEASE_BUTTON_SELECT,
    "UP":pyboy.WindowEvent.RELEASE_ARROW_UP,
    "DOWN":pyboy.WindowEvent.RELEASE_ARROW_DOWN,
    "LEFT":pyboy.WindowEvent.RELEASE_ARROW_LEFT,
    "RIGHT":pyboy.WindowEvent.RELEASE_ARROW_RIGHT
}
def addFrame(image):
    new = frameImage.copy()
    new.paste(image, (68, 61), image.convert("RGBA"))
    return new

if (issueTitle in buttonPresses.keys()):
    # Hold down button in 50 frames
    gameboy.send_input(buttonPresses[issueTitle])
    for i in range(50):
        gameboy.tick()
        images.append(addFrame(gameboy.screen_image()))
    gameboy.send_input(buttonReleases[issueTitle])



images = []
# Run the game for 500 frames (8-ish seconds)
for i in range(500):
    gameboy.tick()
    images.append(addFrame(gameboy.screen_image()))

# Update gifs folder
if os.path.exists("gifs/4.gif"):
    os.remove("gifs/4.gif")
for i in range(3, -1, -1):
    if os.path.exists(f"gifs/{i}.gif"):
        os.rename(f"gifs/{i}.gif", f"gifs/{i+1}.gif")

images[0].save('gifs/0.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=(len(images)/60), loop=0)

# Save state
with open("state_file.state", "wb") as file:
    gameboy.save_state(file)
