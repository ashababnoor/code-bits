import svgutils.transform as sg
import os


def resize_svg(filepath: str, size: tuple['str', 'str'] = ('512', '512'), temp_mode: bool = False) -> str:
    directory = os.path.dirname(filepath)
    input_filename = os.path.basename(filepath)
    if temp_mode:
        output_filename = "tmp_" + input_filename
    else:
        output_filename = "resized_" + input_filename

    output_filepath = os.path.join(directory, output_filename)
    
    fig = sg.fromfile(filepath)
    fig.set_size(size)
    fig.save(output_filepath)

resize_svg('myimage2.svg')