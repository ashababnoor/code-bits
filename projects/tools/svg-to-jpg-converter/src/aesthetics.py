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


def create_abstract_swirl(width, height, *hex_colors):
    # Create a blank image
    img = Image.new('RGB', (width, height), 'white')
    pixels = img.load()

    # Define center and max radius
    cx, cy = width // 2, height // 2
    max_radius = min(cx, cy) - 10

    # Convert hex colors to RGB tuples
    rgb_colors = []
    for hex_color in hex_colors:
        # Remove '#' if present and ensure correct length
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")

        # Convert hex to RGB tuple
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb_colors.append((r, g, b))

    # Generate abstract swirl using given colors
    for x in range(width):
        for y in range(height):
            dx = x - cx
            dy = y - cy
            angle = np.arctan2(dy, dx)
            angle %= 2 * np.pi

            distance = np.sqrt(dx ** 2 + dy ** 2)
            if distance <= max_radius:
                color_idx = int((angle / (2 * np.pi)) * len(rgb_colors)) % len(rgb_colors)
                hue, saturation, value = colorsys.rgb_to_hsv(*[c / 255 for c in rgb_colors[color_idx]])
                saturation = distance / max_radius
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
                pixels[x, y] = (r, g, b)

    # Show or save the image
    # img.show()  # To display the image
    img.save("abstract_swirl.png")  # To save the image as 'abstract_swirl.png'


def main():
    # Provide 3 or 4 hex color codes
    create_abstract_swirl(800, 800, '#FF0000', '#00FF00', '#0000FF')  # For 3 colors
    # create_abstract_swirl(800, 800, '#FF0000', '#00FF00', '#0000FF', '#FFFF00')  # For 4 colors

    # Set the desired width and height
    # create_color_swirl(800, 800)
    
if __name__ == "__main__":
    main()