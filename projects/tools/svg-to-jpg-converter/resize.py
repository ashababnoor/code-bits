import svgutils.transform as sg
from utils import prefix_on_filename


def resize_svg(filepath: str, size: tuple['str', 'str'] = ('512', '512'), temp_mode: bool = False) -> str:
    if temp_mode:
        prefix = "tmp_"
    else:
        prefix = "resized_"

    output_filepath = prefix_on_filename(filepath=filepath, prefix=prefix)
    
    fig = sg.fromfile(filepath)
    fig.set_size(size)
    fig.save(output_filepath)
    return output_filepath


if __name__ == "__main__":
    resize_svg('myimage2.svg')