from PIL import Image
import numpy as np
import colorsys


def create_color_swirl(width, height):
    # Create a blank image
    img = Image.new('RGB', (width, height), 'white')
    pixels = img.load()

    # Define center and max radius
    cx, cy = width // 2, height // 2
    max_radius = min(cx, cy) - 10

    # Generate color swirl
    for x in range(width):
        for y in range(height):
            dx = x - cx
            dy = y - cy
            angle = np.arctan2(dy, dx)
            angle %= 2 * np.pi

            distance = np.sqrt(dx ** 2 + dy ** 2)
            if distance <= max_radius:
                hue = angle / (2 * np.pi)
                saturation = distance / max_radius
                value = 0.9  # Fixed value for brightness
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
                pixels[x, y] = (r, g, b)

    # Show or save the image
    img.save("color_swirl.png")  # To save the image as 'color_swirl.png'

# Set the desired width and height
create_color_swirl(800, 800)