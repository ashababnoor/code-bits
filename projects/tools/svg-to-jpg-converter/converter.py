import cairosvg
from PIL import Image

def convert_svg_to_jpg(input_svg, output_jpg):
    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(url=input_svg, write_to='temp.png')

    # Open the PNG image using PIL
    img = Image.open('temp.png')

    # Calculate dimensions for the new image with 20% padding
    width, height = img.size
    new_width = int(width * 1.4)
    new_height = int(height * 1.4)

    # Create a new white background image
    new_img = Image.new("RGB", (new_width, new_height), "white")

    # Calculate position to center the SVG content
    x_offset = (new_width - width) // 2
    y_offset = (new_height - height) // 2

    # Paste the SVG content onto the white background
    new_img.paste(img, (x_offset, y_offset))

    # Save the final JPG image
    new_img.save(output_jpg, "JPEG")

    # Remove the temporary PNG file
    import os
    os.remove('temp.png')

# Replace 'input.svg' and 'output.jpg' with your file names
convert_svg_to_jpg('input.svg', 'output.jpg')
