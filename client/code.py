# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Capacitive Touch NeoPixel Brightness Control Example"""
import time
import board
import touchio
import neopixel
from rainbowio import colorwheel

touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)
num_pixels = 4
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, auto_write=False)


RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
ORANGE = (255, 44, 0, 0)
TEAL = (0, 128, 128, 0)
MAGENTA = (255, 0, 255, 0)
WHITE = (255, 255, 255, 0)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 254 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def slice_alternating(wait):
    pixels[::2] = [RED] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[1::2] = [ORANGE] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[::2] = [YELLOW] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[1::2] = [GREEN] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[::2] = [TEAL] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[1::2] = [CYAN] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[::2] = [BLUE] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[1::2] = [PURPLE] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[::2] = [MAGENTA] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)
    pixels[1::2] = [WHITE] * (num_pixels // 2)
    pixels.show()
    time.sleep(wait)


pixels.brightness = 0.05
touched = time.monotonic()
color = 0
state = 2

while True:
    if state == 0:
        rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    elif state == 1:
        color_chase(RED, 0.08)  # Increase the number to slow down the color chase
        color_chase(YELLOW, 0.08)
    elif state == 2:
        slice_alternating(0.1)

    if time.monotonic() - touched < 0.15:
        continue
    if touch1.value:
        # Touch pad 1 to increase the brightness.
        pixels.brightness -= 0.05
        pixels.show()
        touched = time.monotonic()
    elif touch2.value:
        # Touch pad 2 to decrease the brightness.
        pixels.brightness += 0.05
        pixels.show()
        touched = time.monotonic()
