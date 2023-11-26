from PIL import Image
import numpy as np
import colorsys
import random


def create_color_swirl(width: int, height: int):
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
            # if distance <= max_radius:
            hue = angle / (2 * np.pi)
            saturation = distance / max_radius
            value = 0.9  # Fixed value for brightness
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            pixels[x, y] = (r, g, b)

    # Show or save the image
    img.save("color_swirl.png")


def create_abstract_swirl(width: int, height: int, hex_colors: list):
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

            color_idx = int((angle / (2 * np.pi)) * len(rgb_colors)) % len(rgb_colors)
            hue, saturation, value = colorsys.rgb_to_hsv(*[c / 255 for c in rgb_colors[color_idx]])
            saturation = distance / max_radius
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            
            pixels[x, y] = (r, g, b)

    # Show or save the image
    # img.show()  # To display the image
    img.save("abstract_swirl.png")
    


def create_spot_pattern(width: int, height: int, hex_colors: list):
    # Create a blank image
    density: int = 5
    
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
    for x in range(0, width, density):
        for y in range(0, height, density):
            if pixels[x, y] == (0, 0, 0):
                continue
            
            dx = x - cx
            dy = y - cy
            angle = np.arctan2(dy, dx)
            angle %= 2 * np.pi

            distance = np.sqrt(dx ** 2 + dy ** 2)
            
            rgb_color = random.choice(rgb_colors)
            # hue, saturation, value = colorsys.rgb_to_hsv(*[c / 255 for c in rgb_color])
            # saturation = distance / max_radius
            # r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            r, g, b = rgb_color
            
            for i in range(density+1):
                for j in range(density+1):
                    if x+i >= width or y+j >= height:
                        continue
                    pixels[x+i, y+j] = (r, g, b)

    # Show or save the image
    # img.show()  # To display the image
    img.save("spots.png")


def main():
    # Set the desired width and height
    # create_color_swirl(800, 800)
    
    # Set the desired width and height and provide 3 or 4 hex color codes
    # create_abstract_swirl(800, 800, ['#FF0000', '#00FF00', '#0000FF'])
    
    # Set the desired width and height and provide 3 or 4 hex color codes
    create_spot_pattern(512, 532, ['#0077b6', '#00b4d8', '#90e0ef'])

    pass
    
if __name__ == "__main__":
    main()