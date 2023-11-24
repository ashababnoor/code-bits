import os
import cairosvg
from PIL import Image

def convert_svg_to_jpg(input_svg, output_jpg=None):
    # Check if the output directory exists, create it if not
    output_dir = os.path.join(os.path.dirname(input_svg), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Determine output file name and path
    if output_jpg is None:
        output_jpg = os.path.join(output_dir, os.path.splitext(os.path.basename(input_svg))[0] + '.jpg')
    else:
        output_jpg = os.path.join(output_dir, output_jpg)

    # Render SVG to a PNG image using cairosvg
    cairosvg.svg2png(url=input_svg, write_to=output_jpg.replace('.jpg', '.png'), dpi=72)

    # Open the rendered PNG image using PIL
    png_img = Image.open(output_jpg.replace('.jpg', '.png'))

    # Calculate dimensions for the new image with 20% padding
    width, height = png_img.size
    new_width = int(width * 1.4)
    new_height = int(height * 1.4)

    # Create a new white background image
    new_img = Image.new("RGB", (new_width, new_height), "white")

    # Calculate position to center the SVG content
    x_offset = (new_width - width) // 2
    y_offset = (new_height - height) // 2

    # Paste the SVG content onto the white background
    new_img.paste(png_img, (x_offset, y_offset))

    # Save the final JPG image
    new_img.save(output_jpg, "JPEG")

    # Remove the temporary PNG file
    os.remove(output_jpg.replace('.jpg', '.png'))



# Replace 'input.svg' with your file name
convert_svg_to_jpg('data/map.svg')  # Output will be saved as 'output/input.jpg'
# or specify output file name
# convert_svg_to_jpg('input.svg', 'output_file_name.jpg')