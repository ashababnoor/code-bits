import os
import cairosvg
from PIL import Image
from resize import resize_svg


def convert_svg_to_jpg(
    input_svg: str, 
    output_jpg: str = None, 
    padding: float = 0, 
    size: tuple = (512, 512)
) -> None:
    """Convert SVG image into JPG format

    Args:
        input_svg (str): Filepath for imput svg image.
        output_jpg (str, optional): Filepath for output jpg image. Defaults to None. When None, output filename is same as input filename with .jpg extension.
        padding (float, optional): Amount of padding to be added on each side. Accepts value between 0 to 1. Defaults to 0.
        size (tuple, optional): Size or dimension of the image in pixels. Defaults to (512, 512).
    """
    # Check if the output directory exists, create it if not
    output_dir = os.path.join(os.path.dirname(input_svg), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Determine output file name and path
    if output_jpg is None:
        output_jpg = os.path.join(output_dir, os.path.splitext(os.path.basename(input_svg))[0] + '.jpg')
    else:
        output_jpg = os.path.join(output_dir, output_jpg)

    # Convert SVG to PNG using cairosvg
    size = tuple(map(str, size))
    resized_input_svg = resize_svg(filepath=input_svg, size=size, temp_mode=True)
    cairosvg.svg2png(url=resized_input_svg, write_to=os.path.join(output_dir, 'temp.png'))

    # Open the PNG image using PIL
    img = Image.open(os.path.join(output_dir, 'temp.png'))

    # Calculate dimensions for the new image with user defined padding
    width, height = img.size
    new_width = int(width * (1 + padding * 2))
    new_height = int(height * (1 + padding * 2))

    # Create a new white background image
    new_img = Image.new(mode="RGB", size=(new_width, new_height), color="white")

    # Calculate position to center the SVG content
    x_offset = (new_width - width) // 2
    y_offset = (new_height - height) // 2

    # Paste the SVG content onto the white background
    new_img.paste(im=img, box=(x_offset, y_offset), mask=img)

    # Save the final JPG image
    new_img.save(output_jpg, "JPEG")

    # Remove the temporary PNG file
    os.remove(os.path.join(output_dir, 'temp.png'))
    os.remove(resized_input_svg)


if __name__ == "__main__":
    convert_svg_to_jpg('data/map.svg', padding=0.3)