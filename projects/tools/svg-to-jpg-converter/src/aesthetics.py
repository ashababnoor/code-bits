from PIL import Image, ImageDraw, ImageOps
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
            hue = angle / (2 * np.pi)
            saturation = distance / max_radius
            value = 0.9  # Fixed value for brightness
            
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            pixels[x, y] = (r, g, b)

    # Show or save the image
    # img.show()  # To display the image
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


def create_spot_pattern(width: int, height: int, hex_colors: list, spiral_saturation: bool = False):
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
            if spiral_saturation:
                hue, saturation, value = colorsys.rgb_to_hsv(*[c / 255 for c in rgb_color])
                saturation = distance / max_radius
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
            else:
                r, g, b = rgb_color
            
            for i in range(density+1):
                for j in range(density+1):
                    if x+i >= width or y+j >= height:
                        continue
                    pixels[x+i, y+j] = (r, g, b)

    # Show or save the image
    # img.show()  # To display the image
    img.save("spots.png")
    

def generate_color_gradient(start_color: int, end_color: int, num_steps: int):
    # Convert hex colors to RGB tuples
    start_r, start_g, start_b = tuple(int(start_color[i:i+2], 16) for i in (0, 2, 4))
    end_r, end_g, end_b = tuple(int(end_color[i:i+2], 16) for i in (0, 2, 4))

    # Calculate step size for each color channel
    step_r = (end_r - start_r) / (num_steps - 1)
    step_g = (end_g - start_g) / (num_steps - 1)
    step_b = (end_b - start_b) / (num_steps - 1)

    # Generate gradient by linear interpolation (lerp) between the colors
    gradient = []
    for i in range(num_steps):
        r = int(start_r + step_r * i)
        g = int(start_g + step_g * i)
        b = int(start_b + step_b * i)
        gradient.append((r, g, b))
    
    return gradient


def create_gradient_image(width: int, height: int, start_color: str, end_color: str):
    # Create a new blank image
    img = Image.new('RGB', (width, height))
    
    # Get color gradient
    gradient = generate_color_gradient(start_color, end_color, max(width, height))

    # Calculate step size for each gradient color
    step = height / len(gradient)

    # Fill the image with the gradient colors
    for i, color in enumerate(gradient):
        start = int(step * i)
        end = int(step * (i + 1))
        for y in range(start, end):
            for x in range(width):
                img.putpixel((x, y), color)

    # Show or save the image
    # img.show()  # To display the image
    img.save("gradient_image.png")
    

def create_gradient_image_with_angle(width: int, height: int, start_color: str, end_color: str, angle: int):
    # Create a new blank image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Get color gradient
    gradient = generate_color_gradient(start_color, end_color, max(width, height))

    # Create a gradient using ImageOps
    gradient_img = Image.new('RGBA', (max(width, height), 1))
    gradient_img.putdata([(r, g, b, 255) for (r, g, b) in gradient])  # Add alpha channel (255 for opaque)
    gradient_img = gradient_img.rotate(-angle, expand=True)

    # Resize the gradient image to match the main image dimensions
    gradient_img = gradient_img.resize((width, height))

    # Paste the gradient onto the main image
    img.paste(gradient_img, box=(0, 0), mask=gradient_img)

    # Save the image
    img.save("gradient_image_with_angle.png")


def main():
    # Set the desired width and height
    # create_color_swirl(800, 800)
    
    # Set the desired width and height and provide hex color codes
    # create_abstract_swirl(800, 800, ['#FF0000', '#00FF00', '#0000FF'])
    
    # Set the desired width and height and provide hex color codes
    # create_spot_pattern(512, 532, ['#0077b6', '#00b4d8', '#90e0ef'])
    
    start_hex_color = 'FF0000'  # Red
    end_hex_color = '0000FF'    # Blue

    # create_gradient_image(512, 512, start_hex_color, end_hex_color)
    create_gradient_image_with_angle(512, 512, start_hex_color, end_hex_color, 70)

    pass
    
if __name__ == "__main__":
    main()