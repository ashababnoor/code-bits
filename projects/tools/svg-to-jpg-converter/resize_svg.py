import xml.dom.minidom
import svgwrite

def resize_svg(input_svg):
    # Parse the SVG file to get width and height
    doc = xml.dom.minidom.parse(input_svg)
    svg_node = doc.getElementsByTagName('svg')[0]
    original_width = svg_node.getAttribute('width')
    original_height = svg_node.getAttribute('height')

    # Remove units from width and height attributes
    original_width = int(original_width.replace('px', '').replace('%', ''))
    original_height = int(original_height.replace('px', '').replace('%', ''))

    # Check if resizing is needed
    if original_width < 512 or original_height < 512:
        # Calculate scaling factors
        scale_x = scale_y = max(512 / original_width, 512 / original_height)

        # Resize the SVG
        dwg = svgwrite.Drawing()
        dwg.add(svgwrite.image.Image(input_svg, insert=(0, 0), size=(original_width * scale_x, original_height * scale_y)))
        
        # Save the resized SVG with the same filename
        output_filename = f"resized_{input_svg}"
        dwg.saveas(output_filename)
        print(f"Resized SVG saved as {output_filename}")
    else:
        print("The SVG is already larger than 512x512")

import svgutils.transform as sg
import sys

fig = sg.fromfile('myimage.svg')
fig.set_size(('200','200'))
fig.save('myimage2.svg')

# Replace 'input.svg' with your file name
resize_svg('map copy.svg')