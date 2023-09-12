from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog
import math
import os
from os.path import join, sep

# Configuration
CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
# CHARS = "@%#*+=-:. "[::-1]
# CHARS = "#Wo- "[::-1]
INIT_DIR = join("C:", sep, "Users", f"{os.environ.get('USERNAME')}", "Pictures")
FONT = ImageFont.truetype(join("C:", sep, "Windows", "Fonts", "lucon.ttf"), 15)
CHAR_W = 10
CHAR_H = 18
TXT_OUT = "output.txt"
IMG_OUT = "output.png"
FACTOR = 1


def file_selection_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.bmp *.jpg *.jpeg")],
        initialdir=INIT_DIR,
        title="Image to ASCII file selection",
    )
    return file_path


def get_image(file_path):
    # Open image file
    if file_path == "":
        file_path = file_selection_dialog()
        if file_path == "":
            print("No image file selected!")
            quit()
    image = Image.open(file_path)
    # Set image to RGB-mode
    if image.mode != "RGB":
        image = image.convert("RGB")
    print("Original size  =", image.width, "x", image.height)
    return resize_image(image)


def resize_image(image):
    # Resize image to maintain aspect-ratio (character-dimension dependent)
    return image.resize(
        (int((image.width / CHAR_W) * FACTOR), int((image.height / CHAR_H) * FACTOR)),
        Image.NEAREST,
    )


def create_output(image):
    # Get pixel data
    pixels = image.load()
    # Create new image
    output_image = Image.new(
        "RGB", (CHAR_W * image.width, CHAR_H * image.height), color=(0, 0, 0)
    )
    # Get draw surface for new image
    d = ImageDraw.Draw(output_image)
    # Create ASCII data and draw onto new image
    with open(TXT_OUT, "w") as f:
        for row in range(image.height):
            for col in range(image.width):
                r, g, b = pixels[col, row]
                intensity = int(r / 3 + g / 3 + b / 3)
                # ASCII conversion
                char = get_char(intensity)
                f.write(char)
                d.text((col * CHAR_W, row * CHAR_H), char, font=FONT, fill=(r, g, b))
            f.write("\n")
    print("Converted size =", output_image.width, "x", output_image.height)
    return output_image


def get_char(intensity):
    # ASCII conversion
    return CHARS[math.floor(intensity * (len(CHARS) / 256))]


def main(file_path=""):

    image = get_image(file_path)

    output_image = create_output(image)

    output_image.save(IMG_OUT)


if __name__ == "__main__":
    main()
