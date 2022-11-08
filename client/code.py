from time import sleep
import board
import touchio
import neopixel
from rainbowio import colorwheel
import supervisor


touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)
num_pixels = 4
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, auto_write=False)


# this function takes a standard "hex code" for a color and returns
# a tuple of (red, green, blue)
def hex2rgb(hex_code):
    red = int("0x" + hex_code[0:2], 16)
    green = int("0x" + hex_code[2:4], 16)
    blue = int("0x" + hex_code[4:6], 16)
    rgb = (red, green, blue)
    # print(rgb)
    return rgb


black = (0, 0, 0)
targetColor = black
curColor = black

mode = "solid"

# We start by turning off pixels
pixels.fill(black)
pixels.show()

# Input is in the format
# index,hexcode,mode,brightness
# where index is the pixel index (0-3)
# hexcode is the color in hex format (RRGGBB)
# mode is either "solid" or "blink"
# brightness is an float between 0 and 1
# Example: 0,FF0000,blink
# This will set pixel 0 to blink red

# This gets a bit complicated so we save a list of dicts for the states
state = []
for i in range(4):
    state.append({"color": black, "mode": "solid", "blink": False})
# Main Loop
while True:
    if supervisor.runtime.serial_bytes_available:
        inText = input().strip()
        if inText == "":
            continue
        print("Received: " + inText)

        # Split the input into the parts
        parts = inText.split(",")
        index = int(parts[0])
        hexcode = parts[1]
        mode = parts[2]

        # Convert the hexcode to RGB
        rgb = hex2rgb(hexcode)

        # Set the state for the pixel
        state[index]["color"] = rgb
        state[index]["mode"] = mode
        state[index]["blink"] = False
    else:
        # Now we update the pixels to the current state
        for i in range(4):
            if state[i]["mode"] == "solid":
                pixels[i] = state[i]["color"]
            elif state[i]["mode"] == "blink":
                if state[i]["blink"]:
                    pixels[i] = state[i]["color"]
                else:
                    pixels[i] = black
                state[i]["blink"] = not state[i]["blink"]
        pixels.show()
        sleep(0.5)
        continue
