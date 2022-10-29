import pyboy

# Load the ROM file
gameboy = pyboy.PyBoy("rom.gb")
gameboy.set_emulation_speed(0)

# Load state
try:
    with open("state_file.state", "rb") as file:
        gameboy.load_state(file)
except Exception as e:
    print("Creating new save")
# Set input
gameboy.send_input(pyboy.WindowEvent.PRESS_BUTTON_A)
gameboy.tick()
gameboy.send_input(pyboy.WindowEvent.RELEASE_BUTTON_A)

images = []
# Run the game for 500 frames (8-ish seconds)
for i in range(500):
    gameboy.tick()
    images.append(gameboy.screen_image())

images[0].save('pillow_imagedraw.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=(len(images)/60), loop=0)

# Save state
with open("state_file.state", "wb") as file:
    gameboy.save_state(file)